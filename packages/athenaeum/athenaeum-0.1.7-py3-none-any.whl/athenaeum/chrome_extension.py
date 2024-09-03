import re
import os
import json
import platform
from typing import Optional, List


class ChromeExtension(object):

    @property
    def user_data_dir(self) -> Optional[str]:
        system = platform.system()
        if system == 'Windows':
            user_data_dir = os.path.expandvars(r'%LOCALAPPDATA%\Google\Chrome\User Data')
        elif system == 'Linux':
            user_data_dir = os.path.expanduser('~/.config/google-chrome')
        elif system == 'Darwin':
            user_data_dir = os.path.expanduser('~/Library/Application Support/Google/Chrome')
        else:
            raise ValueError(f'system：`{system}` 不支持该系统！')
        return user_data_dir

    @property
    def extension_dirs(self) -> List[str]:
        extension_dirs = []

        if not self.user_data_dir:
            return extension_dirs

        pattern = re.compile(r'^[a-z]{32}$')

        extensions_dir = os.path.join(self.user_data_dir, 'Default', 'Extensions')
        for extension_id in os.listdir(extensions_dir):
            extension_dir = os.path.join(extensions_dir, extension_id)
            if pattern.match(extension_id) and os.path.isdir(extension_dir):
                extension_dirs.append(extension_dir)

        return extension_dirs

    @property
    def extension_paths(self) -> List[str]:
        extension_paths = []

        if not self.extension_dirs:
            return extension_paths

        for extension_dir in self.extension_dirs:
            extension_versions = []
            for extension_version in os.listdir(extension_dir):
                if os.path.isdir(os.path.join(extension_dir, extension_version)):
                    extension_versions.append(extension_version)

            latest_extension_version = max(extension_versions)
            extension_path = os.path.join(extension_dir, latest_extension_version)
            extension_paths.append(extension_path)

        return extension_paths

    @property
    def extension_infos(self) -> List[str]:
        extension_infos = []

        if not self.extension_paths:
            return extension_infos

        for extension_path in self.extension_paths:
            manifest_path = os.path.join(extension_path, 'manifest.json')
            if os.path.exists(manifest_path):
                with open(manifest_path, 'r', encoding='utf-8') as f:
                    extension_info = json.load(f)
                    extension_infos.append(extension_info)

        return extension_infos


if __name__ == '__main__':
    ce = ChromeExtension()
    print(ce.user_data_dir)
    print(ce.extension_dirs)
    print(ce.extension_paths)
    print(ce.extension_infos)
