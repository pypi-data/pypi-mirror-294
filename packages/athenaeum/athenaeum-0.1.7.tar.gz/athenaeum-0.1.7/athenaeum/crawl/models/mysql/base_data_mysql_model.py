from athenaeum.crawl.models.base_data_peewee_model import BaseDataPeeweeModel


class BaseDataMysqlModel(BaseDataPeeweeModel):
    _db_type = 'mysql'
