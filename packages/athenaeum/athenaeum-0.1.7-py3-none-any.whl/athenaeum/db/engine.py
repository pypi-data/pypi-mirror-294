from sqlalchemy import create_engine, Engine
from dynaconf.base import LazySettings
from typing import Optional, Dict, Any
from athenaeum.project import get_func_config


def get_mysql_engine(*,
                     settings_object: Optional[LazySettings] = None,
                     func_config_item: Dict[str, Any] = None) -> Optional[Engine]:
    func_config = {
        'MYSQL_USERNAME': None,
        'MYSQL_PASSWORD': None,
        'MYSQL_HOST': None,
        'MYSQL_PORT': None,
        'MYSQL_DBNAME': None,
    }

    func_config = get_func_config(func_config=func_config,
                                  settings_object=settings_object,
                                  func_config_item=func_config_item)
    if func_config is None:
        return

    mysql_uri = 'mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DBNAME}?' \
                'charset=utf8mb4'.format(**func_config)
    mysql_engine = create_engine(mysql_uri)
    return mysql_engine
