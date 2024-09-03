import os
import platform
from typing import List, Tuple


def get_file_paths_and_dir_paths(path: str) -> Tuple[List[str], List[str]]:
    file_paths = []
    dir_paths = []

    with os.scandir(path) as entries:
        for entry in entries:
            system = platform.system()
            if system == 'Windows':
                from nt import DirEntry
            elif system == 'Linux':
                from posix import DirEntry
            elif system == 'Darwin':
                from posix import DirEntry
            else:
                raise ValueError(f'system：`{system}` 不支持该系统！')
            entry: DirEntry
            if entry.is_file():
                file_paths.append(entry.path)
            elif entry.is_dir():
                dir_paths.append(entry.path)
                sub_file_paths, sub_dir_paths = get_file_paths_and_dir_paths(entry.path)
                file_paths.extend(sub_file_paths)
                dir_paths.extend(sub_dir_paths)

    return file_paths, dir_paths
