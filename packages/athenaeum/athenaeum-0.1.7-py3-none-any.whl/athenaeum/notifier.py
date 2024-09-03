import httpx
import yagmail
import tkinter as tk
from tkinter import messagebox
from dynaconf.base import LazySettings
from typing import Optional, Union, Dict, List, Any
from athenaeum.logger import logger
from athenaeum.tools import get_routine_name
from athenaeum.project import get_func_config


class Notifier(object):
    logger = logger

    title = subject = 'athenaeum 通知提醒'
    message = content = '这是一个 `athenaeum 通知提醒` 来自 {}'

    @classmethod
    def notify_by_dingding(cls) -> None:
        method_name = get_routine_name()

    @classmethod
    def notify_by_email(cls, *,
                        settings_object: Optional[LazySettings] = None,
                        func_config_item: Dict[str, Any] = None,
                        **kwargs: Any) -> None:
        func_config = {
            'smtp_username': None,
            'smtp_password': None,
            'smtp_host': None,
        }

        func_config = get_func_config(func_config=func_config,
                                      settings_object=settings_object,
                                      func_config_item=func_config_item)
        if func_config is None:
            return

        method_name = get_routine_name()

        kw = {
            'to': func_config['smtp_username'],
            'subject': cls.subject,
            'contents': cls.content.format(method_name),
        }
        kw.update(kwargs)

        try:
            yag = yagmail.SMTP(**func_config)
            yag.send(**kw)
        except Exception as exception:
            cls.logger.exception(f'邮件发送失败，exception：{exception}！')
        else:
            cls.logger.success('邮件发送成功')

    @classmethod
    def notify_by_bark(cls, *,
                       settings_object: Optional[LazySettings] = None,
                       func_config_item: Dict[str, Any] = None,
                       **kwargs: Any) -> None:
        func_config = {
            'bark_key': None
        }
        func_config = get_func_config(func_config=func_config,
                                      settings_object=settings_object,
                                      func_config_item=func_config_item)
        if func_config is None:
            return

        method_name = get_routine_name()
        title = kwargs.get('title')
        if title is None:
            title = cls.title
        message = kwargs.get('message')
        if message is None:
            message = cls.message.format(method_name)

        try:
            url = f'https://api.day.app/{func_config["bark_key"]}/{title}/{message}'
            _response = httpx.get(url)
        except Exception as exception:
            cls.logger.exception(f'推送发送失败，exception：{exception}！')
        else:
            cls.logger.success('推送发送成功')

    @classmethod
    def notify_by_tkinter(cls, title: Optional[str] = None, message: Optional[str] = None,
                          break_cond: Union[List[Union[None, bool]], Union[None, bool]] = True) -> None:
        method_name = get_routine_name()
        if title is None:
            title = cls.title
        if message is None:
            message = cls.message.format(method_name)

        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        while True:
            result = messagebox.askyesnocancel(title, message)
            if isinstance(break_cond, list):
                if result in break_cond:
                    break
            else:
                if result == break_cond:
                    break

        root.destroy()
