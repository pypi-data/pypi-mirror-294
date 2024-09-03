import inspect
import asyncio
from typing import Optional, Type, Tuple, Dict, Any, Callable, Generator, AsyncGenerator, Union, Coroutine
from athenaeum.crawl.spiders.spider import Spider
from athenaeum.crawl.items.item import Item


async def call_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    if not inspect.isroutine(func):
        raise ValueError(f'func：`{func}` 必须是 `Callable` 对象！')

    if inspect.iscoroutinefunction(func):
        return await func(*args, **kwargs)
    return func(*args, **kwargs)


async def gen_sync_func_result(func_result: Generator) -> AsyncGenerator:
    if not inspect.isgenerator(func_result):
        raise ValueError(f'func_result：`{func_result}` 必须是 `Generator` 对象！')

    while True:
        try:
            yield func_result.__next__()
        except StopIteration as e:
            if e.value is not None:
                yield e.value
            break


class AsyncReturn(Exception):
    def __init__(self, value):
        self.value = value


async def gen_async_func_result(func_result: AsyncGenerator) -> AsyncGenerator:
    if not inspect.isasyncgen(func_result):
        raise ValueError(f'func_result：`{func_result}` 必须是 `AsyncGenerator` 对象！')

    while True:
        try:
            yield await func_result.__anext__()  # python 低版本不支持 `anext(func_result)`
        except AsyncReturn as e:
            yield e.value
            break
        except StopAsyncIteration:
            break


async def gen_sync_async_func_result(func_result: Union[Generator, AsyncGenerator, Coroutine, Any]) -> AsyncGenerator:
    if inspect.isgenerator(func_result) or inspect.isasyncgen(func_result):
        async for item in gen_sync_func_result(func_result) if inspect.isgenerator(func_result) \
                else gen_async_func_result(func_result):
            async for i in gen_sync_async_func_result(item):
                yield i
    else:
        if inspect.iscoroutine(func_result):
            yield await func_result
        else:
            yield func_result


async def gen_func(func: Callable[..., Any], *args: Any, **kwargs: Any) -> AsyncGenerator:
    func_result = await call_func(func, *args, **kwargs)
    async for item in gen_sync_async_func_result(func_result):
        yield item


def crawl(spider_cls: Type[Spider],
          init_args: Optional[Tuple] = None, init_kwargs: Optional[Dict] = None,
          start_requests_args: Optional[Tuple] = None, start_requests_kwargs: Optional[Dict] = None,
          callback: Optional[Callable[[Item], Any]] = None) -> Any:
    if init_args is None:
        init_args = tuple()
    if init_kwargs is None:
        init_kwargs = dict()
    if start_requests_args is None:
        start_requests_args = tuple()
    if start_requests_kwargs is None:
        start_requests_kwargs = dict()

    async def _crawl():
        if not issubclass(spider_cls, Spider):
            raise TypeError(f'spider_cls：`{spider_cls}` 必须是 `athenaeum.crawl.spiders.spider.Spider` 的子类！')
        spider_ins = spider_cls.create_instance(*init_args, **init_kwargs)
        async for item in gen_func(spider_ins.start_requests, *start_requests_args, **start_requests_kwargs):
            if isinstance(item, Item):
                spider_ins.save_item(item)
                if callback is not None:
                    await call_func(callback, item)

    return asyncio.run(_crawl())
