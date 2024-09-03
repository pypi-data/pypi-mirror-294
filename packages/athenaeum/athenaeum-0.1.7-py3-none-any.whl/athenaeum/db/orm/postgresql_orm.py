from peewee import PostgresqlDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_func_config


def get_postgresql_orm(*,
                       settings_object: Optional[LazySettings] = None,
                       func_config_item: Dict[str, Any] = None) -> Any:
    func_config = {
        'host': None,
        'port': None,
        'user': None,
        'password': None,
        'database': None,
    }

    func_config = get_func_config(func_config=func_config,
                                  settings_object=settings_object,
                                  func_config_item=func_config_item)
    if func_config is None:
        return

    postgresql_orm = PostgresqlDatabase(**func_config)
    return postgresql_orm
