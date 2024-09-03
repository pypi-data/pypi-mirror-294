import psutil
from typing import List, Dict, Any
from athenaeum.logger import logger


def kill_process_by_port(port: int) -> None:
    for process in psutil.process_iter():
        for connection in process.connections():
            if connection.laddr.port == port:
                if process.pid != 0:
                    process.kill()
                break


def find_process_pids_by_process_name(process_name: str) -> List[int]:
    process_pids: List[int] = []
    for process in psutil.process_iter(['pid', 'name']):
        process_info: Dict[str, Any] = process.info  # type: ignore
        if not process_name.lower() in process_info['name'].lower():
            continue
        try:
            process_pids.append(process_info['pid'])
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as exception:
            logger.error(f'查找不到 process_name：`{process_name}`，exception: `{exception}`！')
        else:
            logger.success(f'查找到 process_pid：`{process_info["pid"]}`，proc_name：`{process_info["name"]}`')

    logger.success(f'查找到 process_pids: `{process_pids}`')
    return process_pids


def kill_process_by_process_pid(process_pid: int) -> None:
    try:
        proc = psutil.Process(process_pid)
        proc.terminate()
        proc.wait(timeout=3)
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired) as exception:
        logger.error(f'无法杀死 process_pid：`{process_pid}`，exception：`{exception}`！')
    else:
        logger.success(f'已杀死 process_pid：`{process_pid}`')


def kill_process_by_process_name(process_name: str) -> None:
    process_pids = find_process_pids_by_process_name(process_name)
    for process_pid in process_pids:
        kill_process_by_process_pid(process_pid)
