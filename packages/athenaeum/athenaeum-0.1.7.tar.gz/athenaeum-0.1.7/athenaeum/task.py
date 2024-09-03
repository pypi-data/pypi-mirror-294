import time
import random
import threading
import multiprocessing
from typing import Any, Callable
from athenaeum.logger import logger


class Task(object):
    logger = logger

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    start: Callable

    def run(self) -> None:
        while True:
            try:
                self.action()
            except Exception as exception:
                self.logger.exception(f'exception：{exception}！')
                secs = random.uniform(1, 3)
                self.logger.debug(f'休眠{secs:.2f}秒')
                time.sleep(secs)
            else:
                break

    def action(self) -> Any:
        pass


class BaseTask(Task):
    def start(self):
        self.run()


class ThreadTask(Task, threading.Thread):
    pass


class ProcessTask(Task, multiprocessing.Process):
    pass


if __name__ == '__main__':
    task = ProcessTask()
    task.start()
