from athenaeum.logger import logger
from athenaeum.crawl.spiders.mixins.cp_mixin import CpMixin


class BaseCp(CpMixin):
    logger = logger
