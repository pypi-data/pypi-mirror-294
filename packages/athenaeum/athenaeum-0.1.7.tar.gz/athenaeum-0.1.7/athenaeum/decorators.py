import time
import functools
from typing import Callable, Any

from athenaeum.logger import logger


def timeit(func: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.success(f"func：`{func.__name__}` 执行花费 `{end_time - start_time:.4f}` 秒")
        return result

    return wrapper
