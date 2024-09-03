from typing import Union, Tuple, Dict, Set, List
from athenaeum.tools import re_match


class CheckUrlMixin(object):
    """
    example:

        class Example(CheckUrlMixin):
            url_patterns = (
                r'https?://www\.baidu\.com/s\?\S*?wd=(?P<wd>\S+?)(?:&|$)',
                r'https?://www\.so\.com/s\?\S*?q=(\S+?)(?:&|$)'
            )


        example = Example()
        print(example.check_url('https://www.baidu.com/s?wd=Example'))
        print(example.check_url('https://www.so.com/s?q=Example'))

    """
    url_patterns: Union[Tuple[str, ...], Set[str], List[str]]

    def check_url(self, url: str) -> Union[None, Dict[str, str], Tuple[str, ...]]:
        return re_match(url, self.url_patterns)
