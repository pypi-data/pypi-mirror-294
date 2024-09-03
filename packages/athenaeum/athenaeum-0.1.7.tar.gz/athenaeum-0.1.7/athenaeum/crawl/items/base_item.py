from athenaeum.crawl.items.item import Field
from athenaeum.crawl.items.base_data_item import BaseDataItem


class BaseItem(BaseDataItem):
    spider_name = Field()
    spider_source = Field()
    spider_url = Field()
    spider_start_datetime = Field()
    spider_limit_interval = Field()
    spider_run_interval = Field()
    spider_status = Field()
