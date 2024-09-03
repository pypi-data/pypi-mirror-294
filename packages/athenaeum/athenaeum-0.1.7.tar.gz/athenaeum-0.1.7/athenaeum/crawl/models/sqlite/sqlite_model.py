from athenaeum.crawl.models.peewee_model import PeeweeModel


class __SqliteModel(PeeweeModel):
    _db_type = 'sqlite'
