import datetime
from peewee import Model, CharField, SmallIntegerField, DateTimeField, SQL, Field
from typing import Optional, Dict, Any
from athenaeum.crawl.models.peewee_model import PeeweeModel
from athenaeum.metas import merge_metastases
from athenaeum.project import gen_data_id


def set_Fields(cls, db_type):  # noqa
    if db_type == 'mysql':
        if cls.__dict__['data_columns'] is None:
            setattr(cls, 'data_id', CharField(unique=True, max_length=32, verbose_name='数据ID'))
            from playhouse.mysql_ext import JSONField
            setattr(cls, 'data_columns', JSONField(default=['id'], verbose_name='数据字段'))
            setattr(cls, 'status', SmallIntegerField(index=True, default=1, constraints=[SQL('DEFAULT 1')],
                                                     verbose_name='状态'))
            setattr(cls, 'create_time', DateTimeField(index=True, constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')],
                                                      verbose_name='创建时间'))
            setattr(cls, 'update_time', DateTimeField(index=True,
                                                      constraints=[
                                                          SQL('DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP')
                                                      ], verbose_name='更新时间'))
    elif db_type == 'sqlite':
        if cls.__dict__['data_columns'] is None:
            setattr(cls, 'data_id', CharField(unique=True, max_length=32, verbose_name='数据ID'))
            from playhouse.sqlite_ext import JSONField
            setattr(cls, 'data_columns', JSONField(default=['id'], verbose_name='数据字段'))
            setattr(cls, 'status', SmallIntegerField(index=True, default=1, verbose_name='状态'))
            setattr(cls, 'create_time', DateTimeField(index=True, default=datetime.datetime.now,
                                                      verbose_name='创建时间'))
            setattr(cls, 'update_time', DateTimeField(index=True, default=datetime.datetime.now,
                                                      verbose_name='更新时间'))
    else:
        raise ValueError(f'不支持 db_type：`{db_type}`！')


class BaseDataPeeweeModelMeta(type):
    def __new__(cls, name, bases, attrs):
        cls = super().__new__(cls, name, bases, attrs)
        if (_db_type := cls.__dict__['_db_type']) is not None:
            set_Fields(cls, _db_type)
        return cls


class BaseDataPeeweeModel(PeeweeModel, metaclass=merge_metastases(BaseDataPeeweeModelMeta, type(PeeweeModel))):
    # todo: 了解下为啥这里直接赋值 Field 会失败？
    data_id: Optional[Field] = None
    data_columns: Optional[Field] = None
    status: Optional[Field] = None
    create_time: Optional[Field] = None
    update_time: Optional[Field] = None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} id：`{self.id}` data_id：`{self.data_id}`>'

    __str__ = __repr__

    def get_data_id(self) -> str:
        data_columns = self.data.get('data_columns')
        assert (data_columns is not None and isinstance(data_columns, list) and
                all(map(lambda x: isinstance(x, str), data_columns))), '`data_columns` 值必须是字符串列表！'
        for data_column in data_columns:
            if data_column not in self.field_column_names:
                raise ValueError(f'data_columns 中的 `{data_column}` 没有在 '
                                 f'`{self.__class__.__name__}` 中定义该类属性字段！')
            if data_column not in self.data:
                raise ValueError(f'data_columns 中的 `{data_column}` 字段没有赋值，计算得到的 data_id 无效！')
        data_id = self.data.get('data_id')
        if data_id is None:
            data_id = gen_data_id(keys=data_columns, item=self.data)
            self.__data__['data_id'] = data_id
        return data_id

    def get_row_by_data_id(self, data_id: Optional[str] = None) -> Optional[Model]:
        if data_id is None:
            data_id = self.get_data_id()
        return self.get_or_none(self.__class__.data_id == data_id)

    def store(self, data: Optional[Dict[str, Any]] = None) -> bool:
        if data is not None:
            self.data = data
        data_id = self.get_data_id()
        row = self.get_row_by_data_id(data_id)
        if row is None:
            sql = self.insert(**self.data)
            is_insert = True
        else:
            sql = self.update(**self.data).where(self.__class__.data_id == data_id)
            is_insert = False
        with self._meta.database.atomic():
            ret = sql.execute()
            if is_insert:
                self.__data__['id'] = ret
            else:
                if row.__data__.get('id'):
                    self.__data__['id'] = row.__data__.get('id')
        return is_insert
