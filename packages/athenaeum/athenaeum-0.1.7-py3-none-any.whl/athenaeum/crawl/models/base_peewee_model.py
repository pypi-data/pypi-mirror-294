from peewee import CharField, DateTimeField, DecimalField, SmallIntegerField, Field
from typing import Optional
from athenaeum.crawl.models.base_data_peewee_model import BaseDataPeeweeModel
from athenaeum.metas import merge_metastases


def set_Fields(cls, db_type):  # noqa
    setattr(cls, 'spider_name', CharField(index=True, null=True, verbose_name='爬虫名称'))
    setattr(cls, 'spider_source', CharField(null=True, verbose_name='爬虫来源'))
    setattr(cls, 'spider_url', CharField(max_length=2048, null=True, verbose_name='爬虫链接'))
    setattr(cls, 'spider_start_datetime', DateTimeField(null=True, verbose_name='爬虫开始日期时间'))
    setattr(cls, 'spider_limit_interval', DecimalField(decimal_places=2, null=True, verbose_name='爬虫限制间隔时间'))
    setattr(cls, 'spider_run_interval', DecimalField(decimal_places=2, null=True, verbose_name='爬虫运行间隔时间'))
    setattr(cls, 'spider_status', SmallIntegerField(index=True, null=True, verbose_name='爬虫状态'))


class BasePeeweeModelMeta(type):
    def __new__(cls, name, bases, attrs):
        cls = super().__new__(cls, name, bases, attrs)
        if (_db_type := cls.__dict__['_db_type']) is not None:
            set_Fields(cls, _db_type)
        return cls


class BasePeeweeModel(BaseDataPeeweeModel, metaclass=merge_metastases(BasePeeweeModelMeta, type(BaseDataPeeweeModel))):
    # todo: 了解下为啥这里直接赋值 Field 会失败？
    spider_name: Optional[Field] = None
    spider_source: Optional[Field] = None
    spider_url: Optional[Field] = None
    spider_start_datetime: Optional[Field] = None
    spider_limit_interval: Optional[Field] = None
    spider_run_interval: Optional[Field] = None
    spider_status: Optional[Field] = None
