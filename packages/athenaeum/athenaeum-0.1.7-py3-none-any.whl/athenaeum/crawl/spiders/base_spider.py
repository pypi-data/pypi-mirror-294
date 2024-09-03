import inspect
from abc import abstractmethod
from typing import Optional
from athenaeum.metas import merge_metastases
from athenaeum.crawl.spiders.base_data_spider import BaseDataSpider
from athenaeum.project import camel_to_snake


class BaseSpiderMeta(type):

    def __new__(mcs, name, bases, attrs):
        if attrs.get('name') is None:
            attrs['name'] = camel_to_snake(name)
        cls = super().__new__(mcs, name, bases, attrs)
        if not inspect.isabstract(cls):
            if cls.__dict__.get('source') is None:
                raise ValueError(f'`{name}.source` 必须提供！')
            if cls.__dict__.get('url') is None:
                raise ValueError(f'`{name}.url` 必须提供！')
        return cls


class BaseSpider(BaseDataSpider, metaclass=merge_metastases(BaseSpiderMeta, type(BaseDataSpider))):
    name: str
    source: Optional[str] = None
    url: Optional[str] = None
    start_datetime: str = '1998-12-25 00:00:00'
    limit_interval: int = 86400
    run_interval: int = 86400
    status: int = 1

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} name：{self.name}>'

    __str__ = __repr__

    @abstractmethod
    def start_requests(self, *args, **kwargs):
        pass
