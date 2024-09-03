from athenaeum.crawl.models.base_peewee_model import BasePeeweeModel


class BaseSqliteModel(BasePeeweeModel):
    _db_type = 'sqlite'
