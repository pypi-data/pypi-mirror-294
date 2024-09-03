from abc import abstractmethod
from pprint import pformat
from typing import Optional
from athenaeum.crawl.items.base_data_item import BaseDataItem
from athenaeum.crawl.spiders.spider import Spider


class BaseDataSpider(Spider):

    @abstractmethod
    def start_requests(self, *args, **kwargs):
        pass

    def save_item(self, item: Optional[BaseDataItem] = None) -> None:
        if item is None:
            self.logger.debug(f'取消入库操作，item 不能是 None，item：`{item}`')
            return

        if item.is_save is False:
            self.logger.debug(f'取消入库操作，item.is_save 是 False，item：`{item}`')
            return

        if not isinstance(item, BaseDataItem):
            self.logger.debug(f'取消入库操作，item 必须是 BaseDataItem 的实例，item：`{item}`')
            return

        data = item.to_dict()

        model_cls = item.Model
        if model_cls is None:
            raise ValueError(f'model_cls：`{model_cls}` 不能为 None！')
        model_ins = model_cls()
        model_ins.store(data)

        if data['status'] == 1:
            self.logger.success(f'正常数据保存成功，data：`{pformat(data)}`')
        else:
            self.logger.error(f'异常数据保存成功，data：`{pformat(data)}`!')
