import requests
import re
from tqdm import tqdm
from typing import Literal
from bs4 import BeautifulSoup


def search_danbooru_tags(
    name=None,
    category: Literal['artist', 'copyright', 'character', 'general', 'meta'] = None,
    order: Literal['date', 'count', 'name'] = 'date',
    is_deprecated=None,
    hide_empty=True,
    has_wiki=None,
    has_artist=None,
    verbose=False
):
    params = {
        'commit': 'Search',
    }
    if category is not None:
        category_index = {
            'artist': 1,
            'copyright': 2,
            'character': 3,
            'general': 0,
            'meta': 4
        }[category]
        params['search[category]'] = str(category_index)
    if name is not None:
        params['search[name_or_alias_matches]'] = name
    if order is not None:
        params['search[order]'] = order
    if is_deprecated is not None:
        params['search[is_deprecated]'] = 'yes' if is_deprecated else 'no'
    if hide_empty is not None:
        params['search[hide_empty]'] = 'yes' if hide_empty else 'no'
    if has_wiki is not None:
        params['search[has_wiki]'] = 'yes' if has_wiki else 'no'
    if has_artist is not None:
        params['search[has_artist]'] = 'yes' if has_artist else 'no'

    request_url = 'https://danbooru.donmai.us/tags'
    page = 1
    pbar = tqdm(unit=" pages", desc='fetching', disable=not verbose)
    results = []
    while True:
        params['page'] = [str(page)]
        response = requests.get(request_url, params=params)
        if response.status_code != 200:
            pbar.write(f"pp.{page}: " + f"Failed. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        tag_rows = soup.find_all(name='tr', id=re.compile(r'tag-\d+'))
        if not tag_rows:
            pbar.write(f"pp.{page}:", "No tags found")
            break
        result = []
        for tag_row in tag_rows:
            tag_info = {}
            tag_info['name'] = tag_row.find(name='a', class_=re.compile(r'tag-type-[0-4]'), href=re.compile(r"/posts\?tags=.*")).get_text()
            tag_info['id'] = int(tag_row.get('data-id'))
            tag_info['post_count'] = int(tag_row.get('data-post-count'))
            tag_info['category'] = int(tag_row.get('data-category'))
            tag_info['created_at'] = tag_row.get('data-created-at')
            tag_info['updated_at'] = tag_row.get('data-updated-at')
            tag_info['is_deprecated'] = {'false': False, 'true': True}[tag_row.get('data-is-deprecated')]
            result.append(tag_info)
        pbar.write(f"pp.{page}: " + (f"Success. {len(tag_rows)} tags ({result[0]['name']} ~ {result[-1]['name']})" if result else "No tags found"))
        results.extend(result)
        page += 1
        pbar.update(1)
        # paginator-next has not href
        if is_end_page(soup):
            break
    pbar.close()
    results = {tag_info['name']: tag_info for tag_info in results}
    return results


def search_danbooru_artists(name=None, url=None, order: Literal['recently_created', 'last_updated', 'name', 'post_count'] = 'post_count', verbose=False):
    request_url = 'https://danbooru.donmai.us/artists'
    page = 1
    pbar = tqdm(desc="fetching", unit=" pages", disable=not verbose)
    results = []
    while True:
        params = {
            'commit': 'Search',
            'search[order]': order,
            'search[any_name_matches]': name,
            'search[url_matches]': url,
            'page': str(page),
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = requests.get(request_url, params=params)
        if response.status_code != 200:
            pbar.write(f"pp.{page}: " + f"Failed. Status code: {response.status_code}")
        soup = BeautifulSoup(response.text, 'html.parser')
        result = soup.find_all(
            name='a',
            class_='tag-type-1',
        )
        pbar.write(f"pp.{page}: " + (f"Success. {len(result)} tags ({result[0]['name']} ~ {result[-1]['name']})" if result else "No tags found"))
        results.extend(result)
        page += 1
        pbar.update(1)
        if is_end_page(soup):
            break
    pbar.close()
    return [res.get_text() for res in results]


def is_end_page(soup):
    return all(not pn.has_attr('href') for pn in soup.find_all(name='a', class_='paginator-next'))
