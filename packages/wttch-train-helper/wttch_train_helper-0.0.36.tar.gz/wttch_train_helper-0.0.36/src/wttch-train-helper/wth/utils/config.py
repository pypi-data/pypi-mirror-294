import json

import yaml

from wth.log import get_logger


class Config:
    """
    环境配置，使用 yml 文件。
    """

    def __init__(self, key: str, config_file='config.yml'):
        """
        构造函数。
        Args:
            config_file: 配置文件所在位置，默认 config.yml。
        """
        self.config_file = config_file
        self.logger = get_logger("Config")
        self.key = key
        with open(config_file) as f:
            self._original = yaml.load_all(f, Loader=yaml.FullLoader)
            self._active_key = None
            self._shared = {}

            config_map = {}
            for config in self._original:
                config = config['config']
                # 获取激活的环境
                if 'active' in config:
                    self._active_key = config['active']
                    continue
                # 共享的数据
                if 'shared' in config and config['shared']:
                    self._shared = config
                    continue

                if 'name' in config:
                    name = config['name']
                    config_map[name] = config
                else:
                    raise ValueError(f"配置中存在没有 name 的配置. {config}")
            if self._active_key is None:
                raise ValueError("No active config.")
            # 激活的环境
            self._active = config_map[self._active_key]
            if self._active is None:
                raise ValueError("Active config not found.")

            self.logger.info(f"Active config env[{self._active_key}].")
            if len(self._shared) != 0:
                self.logger.info(f"存在共享配置.")

    def __getitem__(self, *items):
        try:
            value = self._active[self.key]
            for item in items:
                value = value[item]
        except (KeyError, ValueError):
            pass
        # 尝试共享获取
        try:
            value = self._shared[self.key]
            for item in items:
                value = value[item]
        except (KeyError, ValueError):
            pass
        return None

    def __str__(self):
        return json.dumps({
            "active": self._active.get(self.key, {}),
            "shared": self._shared.get(self.key, {}),
        })
