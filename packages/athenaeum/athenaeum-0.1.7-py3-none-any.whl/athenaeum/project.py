import re
import hashlib
from copy import deepcopy
from dynaconf.base import LazySettings
from typing import Optional, Any, List, Dict, Literal


def get_func_config(*, func_config: Dict[str, Any],
                    settings_object: Optional[LazySettings] = None,
                    func_config_item: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
    if settings_object is None:
        try:
            from config import settings as settings_object  # type: ignore
        except ModuleNotFoundError:
            pass

    if settings_object is None and func_config_item is None:
        return

    if settings_object is not None:
        for key in func_config.keys():
            func_config[key] = getattr(settings_object, key)

    for key, value in deepcopy(func_config_item).items():
        if key in func_config:
            func_config[key] = value

    return func_config


def camel_to_snake(name: str) -> str:
    """
    >>> camel_to_snake('CamelCaseString')
    'camel_case_string'

    :param name:
    :return:
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def gen_data_id(
        *args: Any,
        keys: Optional[List] = None, item: Optional[Dict] = None,
        algo_type: Literal[
            'md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'blake2b', 'blake2s', 'sha3_224', 'sha3_256', 'sha3_384',
            'sha3_512', 'shake_128', 'shake_256'
        ] = 'md5'
) -> str:
    """
    >>> gen_data_id('123456')
    'e10adc3949ba59abbe56e057f20f883e'

    :param args:
    :param keys:
    :param item:
    :param algo_type:
    :return:
    """
    m = hashlib.new(algo_type)
    if args:
        values = args
    elif keys is not None and item is not None:
        if isinstance(keys, list) and isinstance(item, dict):
            values = [item[k] for k in keys if k in item]
        else:
            raise ValueError('keys 必须是列表，item 必须是字典！')
    elif item is not None:
        values = [item[k] for k in sorted(item.keys())]
    else:
        raise ValueError('args 或 keys 和 item 或 item 必须赋值！')

    data = list(map(lambda x: str(x), values))

    for i in data:
        m.update(i.encode())

    return m.hexdigest()
