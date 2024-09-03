from mongoengine import connect
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_func_config


def get_mongodb_orm(*,
                    settings_object: Optional[LazySettings] = None,
                    func_config_item: Dict[str, Any] = None) -> Any:
    func_config = {
        'host': None,
        'port': None,
        'username': None,
        'password': None,
        'db': None,
    }

    func_config = get_func_config(func_config=func_config,
                                  settings_object=settings_object,
                                  func_config_item=func_config_item)
    if func_config is None:
        return

    mongodb_orm = connect(**func_config)
    return mongodb_orm
