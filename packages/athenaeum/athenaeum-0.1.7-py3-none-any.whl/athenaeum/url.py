import urllib.parse
from furl import furl
from typing import Optional, Dict, List, Any


def get_origin_path(url: str) -> str:
    return f'{furl(url).origin}{furl(url).path}'


def is_valid(url: str) -> bool:
    try:
        result = urllib.parse.urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def quote(url: str) -> str:
    return urllib.parse.quote(url)


def unquote(url: str) -> str:
    return urllib.parse.unquote(url)


def encode(params: Dict[str, str]) -> str:
    return urllib.parse.urlencode(params)


def decode(url: str) -> Dict[str, str]:
    params = dict()
    kvs = url.split('?')[-1].split('&')
    for kv in kvs:
        k, v = kv.split('=', 1)
        params[k] = unquote(v)
    return params


def join_params(url: str, params: Optional[Dict[str, str]] = None) -> str:
    if not params:
        return url
    params = encode(params)
    separator = '?' if '?' not in url else '&'
    return url + separator + params


def get_query_param_value(url: str, key: str, default: Optional[Any] = None) -> str:
    value = furl(url).query.params.get(key, default=default)
    return value


def get_path_segments(url: str) -> List[str]:
    return furl(url).path.segments
