from athenaeum.crawl.items.item import Field, Item


class BaseDataItem(Item):
    id = Field()
    data_id = Field()
    data_columns = Field()
    status = Field()
    create_time = Field()
    update_time = Field()
