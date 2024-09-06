import torch
import numpy as np
import re
import gc
from typing import Dict, Literal, Union, List
from tqdm import tqdm


MODEL = 'model'
CLIP = 'embedders'
CLIP_L = 'embedders.0'
CLIP_G = 'embedders.1'
UNET = 'diffusion_model'
OUT_ALL = 'diffusion_model.output_blocks'
IN_ALL = 'diffusion_model.input_blocks'
MID_ALL = 'diffusion_model.middle_block'
VAE = 'first_stage_model'


StateDict = Dict[str, torch.Tensor]


PRECISION = {
    'bf16': torch.bfloat16,
    'fp16': torch.float16,
    'float': torch.float32,
}


def load_model(model_path, device='cpu'):
    if model_path.endswith('.pt'):
        state_dict = torch.load(model_path, map_location=device)
    elif model_path.endswith('.ckpt'):
        state_dict = torch.load(model_path, map_location=device)
    elif model_path.endswith('.safetensors'):
        import safetensors.torch
        state_dict = safetensors.torch.load_file(model_path, device=device)
    else:
        raise ValueError(f"Unknown model format: {model_path}")
    return state_dict


def save_model(state_dict, model_path):
    if model_path.endswith('.pt'):
        torch.save(state_dict, model_path)
    elif model_path.endswith('.ckpt'):
        torch.save(state_dict, model_path)
    elif model_path.endswith('.safetensors'):
        import safetensors.torch
        safetensors.torch.save_file(state_dict, model_path)
    else:
        raise ValueError(f"Unknown model format: {model_path}")


def clean_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def model_similarity(theta_0: StateDict, theta_1: StateDict, calcmode='cosine_similarity'):
    if calcmode == 'cosine_similarity':
        sim_func = torch.nn.CosineSimilarity(dim=0)
    elif calcmode == 'mse':
        sim_func = torch.nn.MSELoss()
    else:
        raise ValueError(f"Unknown calcmode: {calcmode}")
    keys = [key for key in theta_0.keys()]
    assert all([key in theta_1.keys() for key in keys]), "Missing keys in model B"
    unet_sim = np.array([], dtype=np.float64)
    vae_sim = np.array([], dtype=np.float64)
    clip_l_sim = np.array([], dtype=np.float64)
    clip_g_sim = np.array([], dtype=np.float64)
    for key in tqdm(keys, desc='Stage 1/2'):
        w_0, w_1 = theta_0[key].float(), theta_1[key].float()
        if UNET in key:
            unet_sim = np.append(unet_sim, sim_func(w_0, w_1).cpu().numpy())
        if VAE in key:
            vae_sim = np.append(vae_sim, sim_func(w_0, w_1).cpu().numpy())
        if CLIP_L in key:
            clip_l_sim = np.append(clip_l_sim, sim_func(w_0, w_1).cpu().numpy())
        if CLIP_G in key:
            clip_g_sim = np.append(clip_g_sim, sim_func(w_0, w_1).cpu().numpy())
    return unet_sim.mean(), vae_sim.mean(), clip_l_sim.mean(), clip_g_sim.mean()


def inspect(*theta: StateDict):
    stat = {}
    for t in theta:
        for key, w in tqdm(t.items(), desc='Inspecting'):
            if torch.any(torch.isnan(w)):
                print(f"NaN in {key}")
            mean = w.mean().item()
            std = w.std().item()
            dtype = str(w.dtype)
            if key not in stat:
                stat[key] = {
                    'mean': [],
                    'std': [],
                    'dtype': dtype,
                }
            stat[key]['mean'] = mean
            stat[key]['std'] = std
            stat[key]['dtype'] = dtype
    with open('inspect.json', 'w') as f:
        import json
        json.dump(stat, f, indent=2)
    return stat


def transplant_sd15_clip(sdxl, sd15):
    sd15 = sd15['state_dict']
    sdxl_keys = [key for key in sdxl.keys() if 'text_model' in key]
    sd15_keys = [key for key in sd15.keys() if 'cond_stage_model' in key]

    for sdxl_key in tqdm(sdxl_keys, desc='Transplanting'):
        sd15_key = sdxl_key.replace('conditioner.embedders.0', 'cond_stage_model').replace('text_model.', '')
        if sd15_key not in sd15_keys:
            print(f"Missing key: {sd15_key}")
            continue
        sdxl[sdxl_key] = sd15[sd15_key]
    return sdxl


def merge(
    theta_0: StateDict,
    theta_1: StateDict,
    theta_2: StateDict = None,
    *thetas: StateDict,
    alpha=1,
    algorithm: Literal['normal', 'train_difference', 'normalize', 'zero', 'cosine', 'cosine_diff', 'cosine_train_diff', 'add_cosine_diff', 'cosine_norm', 'cosine_normalize'] = 'normal',
    layers=None,
    verbose=False,
    precision=None,
):
    if isinstance(layers, str):
        layers = [layers]
    if isinstance(alpha, list):
        assert len(alpha) == 23, "Weights of layered merging must be of length 23: 1 for CLIP_L, 1 for CLIP_G, 9 for IN, 3 for MID, and 9 for OUT. But got {} of length {}".format(alpha, len(alpha))
        do_layered_merging = True
        _bm = [False]*len(alpha)
    else:
        do_layered_merging = False

    precision = PRECISION[precision] if precision is not None else None

    keys = [key for key in theta_0.keys() if (not layers or any(idf in key for idf in layers)) and ('weight' in key or 'bias' in key)]
    assert all([key in theta_1.keys() for key in keys]), "Missing keys in model B"
    if theta_2:
        assert all([key in theta_2.keys() for key in keys]), "Missing keys in model C"

    if algorithm in ['cosine', 'cosine_norm', 'cosine_normalize', 'cosine_train_diff', 'add_cosine_diff']:
        cos_sims_01 = {}
        for key in tqdm(keys, desc='Stage 1/2: cosine(0, 1)'):
            w_0, w_1 = theta_0[key].float(), theta_1[key].float()
            w_0_norm = torch.nn.functional.normalize(w_0, p=2, dim=0)
            w_1_norm = torch.nn.functional.normalize(w_1, p=2, dim=0)
            cos_sims_01[key] = torch.cosine_similarity(w_0_norm, w_1_norm, dim=0)
        max_cos_sim_01 = max([v.max() for v in cos_sims_01.values()])
        min_cos_sim_01 = min([v.min() for v in cos_sims_01.values()])

    if algorithm in ('cosine_diff',):
        cos_sims_02 = {}
        for key in tqdm(keys, desc='Stage 1/2: cosine(0, 2)'):
            w_0, w_2 = theta_0[key].float(), theta_2[key].float()
            w_0_norm = torch.nn.functional.normalize(w_0, p=2, dim=0)
            w_2_norm = torch.nn.functional.normalize(w_2, p=2, dim=0)
            cos_sims_02[key] = torch.cosine_similarity(w_0_norm, w_2_norm, dim=0)
        max_cos_sim_02 = max([v.max() for v in cos_sims_02.values()])
        min_cos_sim_02 = min([v.min() for v in cos_sims_02.values()])

    if algorithm in ('cosine_train_diff',):
        cos_sims_12 = {}
        for key in tqdm(keys, desc='Stage 1/2: cosine(1, 2)'):
            w_1, w_2 = theta_1[key].float(), theta_2[key].float()
            w_1_norm = torch.nn.functional.normalize(w_1, p=2, dim=0)
            w_2_norm = torch.nn.functional.normalize(w_2, p=2, dim=0)
            cos_sims_12[key] = torch.cosine_similarity(w_1_norm, w_2_norm, dim=0)
        max_cos_sim_12 = max([v.max() for v in cos_sims_12.values()])
        min_cos_sim_12 = min([v.min() for v in cos_sims_12.values()])

    if algorithm in ('cosine_diff', 'cosine_train_diff'):
        cos_sims_lst = []
        max_cos_sims = []
        min_cos_sims = []
        for i, theta in enumerate(thetas):
            cos_sims = {}
            for key in tqdm(keys, desc='Stage 1/2: cosine(0, {})'.format(i+3)):
                w_0, w_i = theta_0[key].float(), theta[key].float()
                w_0_norm = torch.nn.functional.normalize(w_0, p=2, dim=0)
                w_i_norm = torch.nn.functional.normalize(w_i, p=2, dim=0)
                cos_sims[key] = torch.cosine_similarity(w_0_norm, w_i_norm, dim=0)
            cos_sims_lst.append(cos_sims)
            max_cos_sims.append(max([v.max() for v in cos_sims.values()]))
            min_cos_sims.append(min([v.min() for v in cos_sims.values()]))

    for key in tqdm(keys, desc='Stage 2/2'):
        if VAE in key:
            continue
        dtype = precision or theta_0[key].dtype
        w_0, w_1 = theta_0[key].float(), theta_1[key].float()
        w_2 = theta_2[key].float() if theta_2 else None
        ws = [theta[key].float() for theta in thetas]

        if do_layered_merging:
            a = None
            clip_match = re.search(r'\.embedders\.(0|1)\.', key)
            if clip_match:
                block_id = int(clip_match.group(1))
                block = 'clip_l' if block_id == 0 else 'clip_g'
                idx = block_id
                a = alpha[idx]
            dm_match = re.search(r'\.(input_blocks|middle_block|output_blocks)\.(\d+)\.', key)
            if not a and dm_match:
                block, block_id = dm_match.groups()
                block_id = int(block_id)
                idx = block_id + (2 if block == 'input_blocks' else 11 if block == 'middle_block' else 14)
                a = alpha[idx]
            if not a:
                continue
            if verbose and a and not _bm[idx]:
                print(f"alpha[{block:<12}][{block_id}] = {a:<.4f}")
                _bm[idx] = True
        else:
            a = alpha

        if algorithm == 'normal':
            if a == 1:
                theta_0[key] = w_1
                continue
            elif a == 0:
                continue

        if algorithm == 'normal':
            # Weighted average
            w = w_1 * a + w_0 * (1 - a)
        elif algorithm == 'normalize':
            k = w_0 * torch.norm(w_1) / torch.norm(w_0)
            # k = w_0 + w_1*cos_sims[key]
            w = k
        elif algorithm == 'cosine_norm':
            # Cosine similarity
            k = (1 - cos_sims_01[key]) / 2  # The higher, the more similar
            k = (k - min_cos_sim_01) / (max_cos_sim_01 - min_cos_sim_01)
            a *= k
            w = w_1 * a + w_0 * (1 - a)
        elif algorithm == 'cosine':
            # Cosine similarity
            k = (1 - cos_sims_01[key]) / 2  # similar is smaller
            a *= k
            w = w_1 * a + w_0 * (1 - a)
        elif algorithm == 'cosine_normalize':
            k = w_0 * torch.norm(cos_sims_01[key]*w_1) / torch.norm(w_0)
            # k = w_0 + w_1*cos_sims[key]
            w = k
        elif algorithm == 'cosine_diff':
            assert theta_2, "Missing model C"
            k = cos_sims_02[key]
            k = (k - min_cos_sim_02) / (max_cos_sim_02 - min_cos_sim_02)  # normalize to [0, 1]
            for i, cos_sims in enumerate(cos_sims_lst):
                k_i = (cos_sims[key] - min_cos_sims[i]) / (max_cos_sims[i] - min_cos_sims[i])
                k *= k_i
            k *= a
            w = w_0 * k + w_1 * (1 - k)
        elif algorithm == 'cosine_train_diff':
            # Cosine Train difference
            assert theta_2, "Missing model C"
            diff_01 = 1 - (cos_sims_01[key] - min_cos_sim_01) / (max_cos_sim_01 - min_cos_sim_01)
            diff_12 = 1 - (cos_sims_12[key] - min_cos_sim_12) / (max_cos_sim_12 - min_cos_sim_12)

            diffs = []
            for i, cos_sims in enumerate(cos_sims_lst):
                diff_i = 1 - (cos_sims[key] - min_cos_sims[i]) / (max_cos_sims[i] - min_cos_sims[i])
                diffs.append(diff_i)

            sum_dist = torch.abs(diff_01) + torch.abs(diff_12) + sum([torch.abs(diff_i) for diff_i in diffs])
            scale = torch.where(sum_dist != 0, torch.abs(diff_01) / sum_dist, torch.tensor(0.).float())

            w = w_0 + ((len(ws) + 1) * w_1 - w_2 - sum(ws)) * scale * a * 1.8
        elif algorithm == 'add_cosine_diff':
            diff_01 = 1 - (cos_sims_01[key] - min_cos_sim_01) / (max_cos_sim_01 - min_cos_sim_01)  # normalize to [0, 1]
            scale = diff_01
            w_diff = w_1 - w_0
            w = w_0 * (1 - scale) + w_diff * scale * a * 1.8

        elif algorithm == 'train_difference':
            # Train difference
            assert theta_2, "Missing model C"
            if torch.allclose(w_1, w_2):
                continue
            diff_10 = w_1 - w_0
            diff_12 = w_1 - w_2
            sum_dist = torch.abs(diff_10) + torch.abs(diff_12)
            scale = torch.where(sum_dist != 0, torch.abs(diff_10) / sum_dist, torch.tensor(0.).float())
            w = w_0 + diff_12 * scale * a * 1.8
        elif algorithm == 'zero':
            if w_1.mean().item() < 1e-6:
                print(f"Zeroing {key}")
                w = w_1
            else:
                w = w_0

        w = w.to(dtype=dtype)
        theta_0[key] = torch.where(torch.isnan(w), torch.zeros_like(w), w)
        # Check nan
        assert not torch.isnan(theta_0[key]).any(), f"NaN found in {key}"
        clean_memory()
    return theta_0


# def merge(
#     *models,
#     algorithm: Literal['normal', 'cosine'],
#     layers: List[str],
# ):
