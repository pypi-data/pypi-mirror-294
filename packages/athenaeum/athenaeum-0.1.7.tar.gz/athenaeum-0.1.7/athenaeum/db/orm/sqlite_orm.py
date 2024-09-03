from peewee import SqliteDatabase
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_func_config


def get_sqlite_orm(*,
                   settings_object: Optional[LazySettings] = None,
                   func_config_item: Dict[str, Any] = None) -> Any:
    func_config = {
        'database': None
    }

    func_config = get_func_config(func_config=func_config,
                                  settings_object=settings_object,
                                  func_config_item=func_config_item)
    if func_config is None:
        return

    sqlite_orm = SqliteDatabase(**func_config)
    return sqlite_orm
