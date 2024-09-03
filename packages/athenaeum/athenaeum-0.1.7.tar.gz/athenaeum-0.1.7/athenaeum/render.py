import os
import jinja2
import shutil
from typing import Optional, Dict
from athenaeum.file import get_file_paths_and_dir_paths
from athenaeum.logger import logger


class Render(object):
    logger = logger

    athenaeum_dir_path = os.path.dirname(os.path.abspath(__file__))
    templates_dir_path = os.path.join(athenaeum_dir_path, 'templates')
    project_dir_path = os.path.join(templates_dir_path, 'project')
    cwd_dir_path = os.getcwd()

    @classmethod
    def render_template(cls, *, file_path: Optional[str] = None,
                        file_name: Optional[str] = None, dir_path: Optional[str] = None,
                        render_data: Optional[Dict[str, str]] = None,
                        render_file_path: Optional[str] = None) -> str:
        if file_path is None and (file_name is None or dir_path is None):
            raise ValueError(f'file_path：`{file_path}` 或 file_name：`{file_name}` 和 dir_path：`{dir_path}` 必须赋值！')

        if render_data is None:
            render_data = dict()

        if file_path is not None:
            file_name = os.path.basename(file_path)
            dir_path = os.path.dirname(file_path)

        loader = jinja2.FileSystemLoader(searchpath=dir_path)
        env = jinja2.Environment(loader=loader)
        template = env.get_template(name=file_name)
        result = template.render(**render_data)

        if render_file_path is not None:
            with open(render_file_path, 'w', encoding='utf-8') as f:
                f.write(result)

        return result

    @classmethod
    def render_project(cls, *, project_name: str) -> None:
        data = {
            'project_name': project_name
        }
        file_paths, dir_paths = get_file_paths_and_dir_paths(cls.project_dir_path)
        for file_path in file_paths:
            src_file_path = file_path
            dest_file_path = os.path.join(cls.cwd_dir_path, os.path.relpath(src_file_path, cls.project_dir_path))
            try:
                dest_dir_path = os.path.dirname(dest_file_path)
                os.makedirs(dest_dir_path, exist_ok=True)
                dest_file_name = os.path.basename(dest_file_path)
                dest_file_prefix, dest_file_suffix = os.path.splitext(dest_file_name)
                if dest_file_suffix == '.jinja2':
                    dest_file_path = os.path.join(dest_dir_path, dest_file_prefix)
                    if not os.path.exists(dest_file_path):
                        cls.render_template(file_path=src_file_path, render_data=data, render_file_path=dest_file_path)
                        cls.logger.success(f'成功渲染：`{src_file_path}` -> `{dest_file_path}`')
                    else:
                        cls.logger.warning(f'取消渲染（文件已存在）：`{src_file_path}` -> `{dest_file_path}`')
                else:
                    if not os.path.exists(dest_file_path):
                        shutil.copy(src_file_path, dest_file_path)
                        cls.logger.success(f'成功拷贝：`{src_file_path}` -> `{dest_file_path}`')
                    else:
                        cls.logger.warning(f'取消拷贝（文件已存在）：`{src_file_path}` -> `{dest_file_path}`')
            except Exception as exception:
                cls.logger.exception(f'执行出错，exception：`{exception}`！')
