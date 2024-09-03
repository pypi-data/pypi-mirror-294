from abc import ABCMeta
from collections.abc import MutableMapping
from pprint import pformat
from typing_extensions import Self
from typing import Iterator, Optional, Dict, Type, Any
from athenaeum.crawl.models.model import Model
from athenaeum.crawl.errors import ItemInitError, ItemGetAttributeError
from athenaeum.metas import merge_metastases, BasesAttrsMergeMeta


class Field(object):
    pass


class ItemMeta(type):
    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        attrs = cls.__dict__
        cls._Fields = {key: value for key, value in attrs.items() if isinstance(value, Field)}
        return cls


class Item(MutableMapping, metaclass=merge_metastases(ItemMeta, BasesAttrsMergeMeta, ABCMeta)):
    _Fields: Optional[Dict]

    def __init__(self, *args, **kwargs):
        self._data = dict()
        self.is_save: Optional[bool] = None
        self.Model: Optional[Type[Model]] = None

        if args:
            raise ItemInitError('请使用关键词参数！')
        if kwargs:
            for k, v in kwargs.items():
                self._data[k] = v

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} _data：{pformat(dict(self._data))}>'

    __str__ = __repr__

    def __setitem__(self, key, value) -> None:  # MutableMapping
        if key in self._Fields:
            self._data[key] = value
        else:
            raise KeyError(f'请在 {self.__class__.__name__} 类中定义 `{key} = Field()`！')

    def __delitem__(self, key) -> None:  # MutableMapping
        del self._data[key]

    def __getitem__(self, key) -> Any:  # Mapping
        return self._data[key]

    def __len__(self) -> int:  # Collection
        return len(self._data)

    def __iter__(self) -> Iterator:  # Iterable
        return iter(self._data)

    def __setattr__(self, key, value) -> None:
        if key not in ['_data', 'is_save', 'Model']:
            raise AttributeError(f'请使用 `item[{key!r}] = {value!r}` 来赋值！')
        super().__setattr__(key, value)

    def __getattr__(self, key) -> None:
        raise AttributeError(f'key：`{key}` 不能获取不存在的属性！')

    def __getattribute__(self, key) -> Any:
        _Fields = super().__getattribute__('_Fields')
        if key in _Fields:
            raise ItemGetAttributeError(f'请使用 `{self.__class__.__name__} 的实例对象[{key!r}]` 来获取值！')
        return super().__getattribute__(key)

    def to_dict(self) -> dict:
        return dict(self._data)

    def copy(self) -> Self:
        ins = self.__class__(**self._data)
        ins.is_save = self.is_save
        ins.Model = self.Model
        return ins
