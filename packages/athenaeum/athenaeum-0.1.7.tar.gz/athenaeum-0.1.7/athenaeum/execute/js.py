import execjs
import py_mini_racer
from typing import Optional, Any


def execute_js_code_by_PyExecJS(js_code: str, func_name: Optional[str] = None,  # noqa
                                *args: Any, **kwargs: Any) -> Any:
    if func_name is None:
        ctx = execjs.compile(js_code)
        result = ctx.eval(js_code)
    else:
        ctx = execjs.compile(js_code)
        result = ctx.call(func_name, *args, **kwargs)
    return result


def execute_js_code_by_py_mini_racer(js_code: str, func_name: Optional[str] = None,
                                     *args: Any, **kwargs: Any) -> Any:
    if func_name is None:
        ctx = py_mini_racer.MiniRacer()
        result = ctx.eval(js_code)
    else:
        ctx = py_mini_racer.MiniRacer()
        ctx.eval(js_code)
        result = ctx.call(func_name, *args, **kwargs)
    return result
