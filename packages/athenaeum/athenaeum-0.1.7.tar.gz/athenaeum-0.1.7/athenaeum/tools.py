import re
import time
import tqdm
import ujson
import inspect
import sqlparse
from htmlmin import minify
from typing import Union, Dict, Any, Tuple, Set, List, Protocol
from athenaeum.execute.js import execute_js_code_by_py_mini_racer


def format_price(price: Union[int, float, str], places: int = 2) -> str:
    """
    >>> format_price(3.1)
    '3.10'

    :param price:
    :param places:
    :return:
    """
    integer_str, decimal_str = str(float(price)).split('.')
    decimal_str = (decimal_str + '0' * (places - len(decimal_str)))[:places]
    price_str = '.'.join([integer_str, decimal_str])
    return price_str


def jsonp_to_json(jsonp: str) -> Dict[str, Any]:
    func_name = re.match(r'(?P<func_name>jQuery.*?)\(\{.*\}\)\S*', jsonp).groupdict()['func_name']
    js_code = f'''function {func_name}(o){{return o}};function sdk(){{return JSON.stringify({jsonp})}};'''
    json_str = execute_js_code_by_py_mini_racer(js_code, func_name='sdk')
    json_obj = ujson.loads(json_str)
    return json_obj


def chunk_data(data: List[Any], chunk_size: int) -> List[List[Any]]:
    return [data[i: i + chunk_size] for i in range(0, len(data), chunk_size)]


def compressed_html(html: str, **kwargs: Any) -> str:
    return minify(html, **kwargs)


def format_sql(sql: str, **kwargs) -> str:
    kw = dict(reindent=True,
              keyword_case='upper',
              identifier_case='lower',
              strip_comments=True)
    kw.update(kwargs)
    sql = sqlparse.format(sql, **kw)
    return sql


class Container(Protocol):
    def __init__(self, database, key):
        self.database = database
        self.key = key

    def __len__(self) -> int:
        pass


def show_progress(container: Container, frequency: float = 1.0) -> None:
    total_num = len(container)
    desc = f'database：{container.database}，key：{container.key} 消费速度'
    unit = '条'

    bar = tqdm.tqdm(desc=desc, total=total_num, leave=True, unit=unit)

    sum_num = 0
    while True:
        now_num = len(container)
        pass_num = total_num - now_num
        update_num = pass_num - sum_num
        sum_num += update_num

        bar.update(update_num)

        if sum_num == total_num:
            break

        time.sleep(frequency)


def get_routine_name() -> str:
    return inspect.stack()[1][3]


def re_match(string: str, patterns: Union[Tuple[str, ...], Set[str], List[str]]) -> \
        Union[None, Dict[str, str], Tuple[str, ...]]:
    if not patterns:
        return

    if not ((isinstance(patterns, tuple) or isinstance(patterns, set) or isinstance(patterns, list)) and
            all(map(lambda x: isinstance(x, str), patterns))):
        raise ValueError(f'patterns：`{patterns}` 赋值错误，其值只能是字符串元组或字符串集合或字符串列表！')

    compilers = [re.compile(pattern) for pattern in patterns]
    for compiler in compilers:
        match = compiler.match(string)
        if match is None:
            continue
        groupdict = match.groupdict()  # noqa
        if groupdict:
            return groupdict
        groups = match.groups()
        if groups:
            return groups
        return

    raise ValueError(f'string：`{string}` 没有匹配 patterns：`{patterns}`！')
