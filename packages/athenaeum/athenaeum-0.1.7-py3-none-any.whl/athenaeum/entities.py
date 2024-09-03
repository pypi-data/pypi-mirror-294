import random
from dataclasses import dataclass
from dynaconf.base import LazySettings
from typing_extensions import Self
from typing import Optional, Dict, Any
from athenaeum.project import get_func_config


@dataclass
class AccountEntity(object):
    """
    使用教程：
        /project/settings/settings.toml

        [default.account.baidu.user1]
        owner = "xxx"
        username = "111111"
        password = "999999"

        [default.account.360.user1]
        owner = "yyy"
        username = "222222"
        password = "888888"

    """
    platform: str
    owner: str
    username: str
    password: str

    @classmethod
    def get_a_random_account_entity(cls, *,
                                    settings_object: Optional[LazySettings] = None,
                                    func_config_item: Dict[str, Any] = None,
                                    **kwargs: Any) -> Optional[Self]:
        func_config = {
            'account': None,
        }

        func_config = get_func_config(func_config=func_config,
                                      settings_object=settings_object,
                                      func_config_item=func_config_item)
        if func_config is None:
            return

        platform = kwargs['platform']

        users = func_config['account'][platform]
        user = users[random.choice(list(users.keys()))]
        return cls(
            platform=platform,
            owner=user.owner,
            username=user.username,
            password=user.password
        )
