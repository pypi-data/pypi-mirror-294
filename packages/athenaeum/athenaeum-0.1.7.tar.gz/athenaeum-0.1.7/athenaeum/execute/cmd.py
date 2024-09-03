import subprocess
from typing import Optional
from athenaeum.logger import logger


def execute_cmd(cmd: str, encoding: str = 'utf-8') -> Optional[bool]:
    result = None
    try:
        process = subprocess.Popen(cmd, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding=encoding)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            logger.success(f'cmd：`{cmd}`，运行成功')
            result = stdout
        else:
            logger.error(f'cmd：`{cmd}`，运行失败！')
            result = False
    except Exception as exception:
        logger.exception(f'cmd：`{cmd}` 未知错误，exception：{exception}！')
        result = False
    finally:
        return result
