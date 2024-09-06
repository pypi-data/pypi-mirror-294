import subprocess
import os
from typing import Optional, List, Union, Dict, Tuple, Callable
from pathlib import Path
from waifuset import logging

logger = logging.get_logger(name="gallery-dl", disable=False)


def download_by_tags(
    tags: Union[str, List[str], Dict[str, Union[int, Tuple[int, int]]]],
    config_path: Optional[str] = None,
    base_directory: Optional[str] = None,
    archive_path: Optional[str] = None,
    start: int = 1,
    end: int = 2000,
    quiet: bool = False,
    naming_func: Callable[[str], str] = lambda x: x,
    username: Optional[str] = None,
    password: Optional[str] = None,
):
    r"""
    Download images from danbooru using gallery-dl.
    @param tags: tags to download, can be a string, a list of strings, or a dictionary of strings to ranges.
    """
    if isinstance(tags, str):
        tags = {tags: (start, end)}
    elif isinstance(tags, list):
        tags = {tag: (start, end) for tag in tags}
    elif isinstance(tags, dict):
        for tag, range in tags.items():
            if isinstance(range, int):
                tags[tag] = (start, start + range - 1)
            elif isinstance(range, tuple):
                lo, hi = range
                lo = lo if lo is not None else start
                hi = hi if hi is not None else end
                tags[tag] = (lo, hi)
            elif range is None:
                tags[tag] = (start, end)
            else:
                raise ValueError(f"invalid range: {range}")
    else:
        raise ValueError(f"invalid tags: {tags}")
    if config_path is not None:
        config_path = Path(config_path).as_posix()
        assert os.path.exists(config_path), f"config path not found: {config_path}"
        logger.print(f"config path: {logging.yellow(config_path)}")

    logger.print(f"tag list:")
    logger.print(f"  '\n  ".join([f"{tag}: {range}" for tag, range in tags.items()]), no_prefix=True)

    tags = {tag.strip().lower().replace(' ', '_'): range for tag, range in tags.items()}
    pbar = logger.tqdm(total=len(tags), desc="download")
    for tag, range in tags.items():
        logger.print(f"tag: {tag} | range: {range}")
        url = f"https://danbooru.donmai.us/posts?tags={tag}"
        category = tag.replace('_', ' ').replace(':', ' ').replace('/', '').replace('\\', '')
        category = naming_func(category)
        pbar.set_postfix({'tag': tag, 'category': category})
        # get command
        command = [
            "gallery-dl",
            "-o",
            f"extractor.danbooru.directory=[\"{category}\"]",
            "--no-part",
            "--range",
            f"{range[0]}-{range[1]}",
        ]
        if username is not None and password is not None:
            command += ["-o", f"extractor.danbooru.username=\"{username}\""]
            command += ["-o", f"extractor.danbooru.password=\"{password}\""]
        if base_directory is not None:
            command += ["-o", f"extractor.danbooru.base-directory=[\"{Path(base_directory).as_posix()}\"]"]
        if archive_path is not None:
            command += ["-o", f"extractor.danbooru.archive=[\"{Path(archive_path).as_posix()}\"]"]
        if config_path is not None:
            command += ["-c", Path(config_path).as_posix()]
        if quiet:
            command += ["-q"]
        command.append(url)
        # download!
        while True:
            try:
                process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)
                for line in iter(process.stdout.readline, ''):
                    print(line, end='')
                process.stdout.close()
                return_code = process.wait()
                if return_code != 0:
                    raise subprocess.CalledProcessError(return_code, command)
                break
            except subprocess.CalledProcessError as e:
                logger.error(f"error: {e}")
                continue
            except KeyboardInterrupt:
                raise
        pbar.update(1)
    pbar.close()
