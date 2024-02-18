# -*- coding: utf-8 -*-
"""
@File: log2.py
@Author: ltw
@Time: 2024/1/5

logging配置初始化, 仅提供函数, 不实际调用
注意事项: 需在项目入口初始化
使用示例:
    from xlogging.log import LogMethods
    from xlogging.config import StatisticLogConfig

    LogMethods.config(StatisticLogConfig)
"""
import logging.config
import traceback
from pathlib import Path
from typing import Type, TypeVar

from .config import LogConfig

# LogConfigBase类及其子类
TypeLogConfig = TypeVar("TypeLogConfig", bound=LogConfig)


class LogMethods:
    """
    singleton Log
    """

    @classmethod
    def config(cls, log_config: Type[TypeLogConfig]):
        """应用log配置"""
        cls.make_path(log_config)
        logging.config.dictConfig(log_config.dict_config())
        logging.info(
            "<LogMethods> dictConfig load %s", log_config.dict_config()
        )

    @staticmethod
    def make_path(config):
        """
        检查日志输出文件路径, 不存在则创建
        """
        handlers_config = config.dict_config().get("handlers", {})
        if not handlers_config:
            return
        file_paths = []
        for _, configs in handlers_config.items():
            for cfg_key, val in configs.items():
                if cfg_key != "filename":
                    continue
                file_paths.append(val)
        try:
            for path in file_paths:
                path_obj = Path(path)
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                path_obj.touch(exist_ok=True)
        except OSError as _e:
            traceback.print_exc()
