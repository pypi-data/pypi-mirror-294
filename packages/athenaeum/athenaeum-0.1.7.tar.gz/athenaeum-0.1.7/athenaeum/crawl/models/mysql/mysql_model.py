from athenaeum.crawl.models.peewee_model import PeeweeModel


class MysqlModel(PeeweeModel):
    _db_type = 'mysql'
