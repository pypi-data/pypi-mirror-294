import threading
import multiprocessing
from pathlib import Path
from dynaconf import Dynaconf
from athenaeum.logger import logger

ROOT_DIR = Path(__file__).absolute().parent

FILES_DIR = ROOT_DIR / 'files'
FILES_DIR.mkdir(exist_ok=True)

MODELS_DIR = ROOT_DIR / 'models'
MODELS_DIR.mkdir(exist_ok=True)

ITEMS_DIR = ROOT_DIR / 'items'
ITEMS_DIR.mkdir(exist_ok=True)

SETTINGS_DIR = ROOT_DIR / 'settings'
SETTINGS_DIR.mkdir(exist_ok=True)

settings_files = [
    str(SETTINGS_DIR / 'settings.toml'),
    str(SETTINGS_DIR / 'settings.dev.toml'),
    str(SETTINGS_DIR / 'settings.prod.toml'),
]
dotenv_path = str(ROOT_DIR / '.env')

settings = Dynaconf(
    settings_files=settings_files,
    dotenv_path=dotenv_path,
    envvar_prefix='DYNACONF',
    env_switcher='DYNACONF_ENV',
    environments=True,
    load_dotenv=True,
)

settings.ROOT_DIR = ROOT_DIR
settings.FILES_DIR = FILES_DIR
settings.MODELS_DIR = MODELS_DIR
settings.ITEMS_DIR = ITEMS_DIR
settings.SETTINGS_DIR = SETTINGS_DIR

logger.debug(f'当前线程名：`{threading.current_thread()}`，'
             f'当前进程名：`{multiprocessing.current_process()}`，'
             f'当前环境：`{settings.current_env}`')

__all__ = [
    'settings'
]
