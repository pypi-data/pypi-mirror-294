from athenaeum.crawl.models.base_peewee_model import BasePeeweeModel


class BaseMysqlModel(BasePeeweeModel):
    _db_type = 'mysql'
