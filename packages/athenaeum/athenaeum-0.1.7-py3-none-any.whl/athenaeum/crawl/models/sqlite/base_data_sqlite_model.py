from athenaeum.crawl.models.base_data_peewee_model import BaseDataPeeweeModel


class BaseDataSqliteModel(BaseDataPeeweeModel):
    _db_type = 'sqlite'
