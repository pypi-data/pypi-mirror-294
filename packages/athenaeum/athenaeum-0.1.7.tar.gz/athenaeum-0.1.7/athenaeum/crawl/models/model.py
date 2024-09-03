import peewee
from abc import ABCMeta, abstractmethod
from athenaeum.metas import merge_metastases, BasesAttrsMergeMeta
from typing import Optional, Dict, Any


class ModelMeta(type):
    def __subclasscheck__(cls, subclass):
        if issubclass(subclass, peewee.Model):  # 只要是指定 Model：peewee.Model 的子类，就认定为是本 Model 的子类
            return True
        return False


class Model(metaclass=merge_metastases(ModelMeta, BasesAttrsMergeMeta, ABCMeta)):  # model 判断是否合法用，不被继承

    @abstractmethod
    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        pass
