# -*- coding: utf-8 -*-
"""
@File: log
@Author: ltw
@Time: 2023/2/6

logger 默认设置
"""
import logging.config
from pathlib import Path
from .config import LogConfig


def root_log(msg):
    """
    root logger
    """
    logger = logging.getLogger()
    logger.warning(msg)


class Log:
    """
    singleton Log
    """

    _instance = None
    _init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_config=LogConfig):
        if self._init:
            return
        self._init = True
        # 日志配置初始化
        self.config = log_config
        self.make_path()
        logging.config.dictConfig(self.config.dict_config())
        root_log("logger init")

    def make_path(self):
        """
        检查日志输出文件路径, 不存在则创建
        """
        handlers_config = self.config.dict_config().get("handlers", {})
        if not handlers_config:
            return
        file_paths = []
        for _, configs in handlers_config.items():
            for cfg_key, val in configs.items():
                if cfg_key != "filename":
                    continue
                file_paths.append(val)
        for path in file_paths:
            path_obj = Path(path)
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            path_obj.touch(exist_ok=True)

    def local_logger(self):
        """
        local_logger
        :return:
        """
        return logging.getLogger(self.config.LOCAL_LOGGER_NAME)

    def debug_logger(self):
        """
        debug_logger
        :return:
        """
        return logging.getLogger(self.config.DEBUG_LOGGER_NAME)

    def local_log(self, msg):
        """
        正常滚动日志 输出路径见 config.LOG_FILE
        :return:
        """
        logger = self.local_logger()
        logger.info(msg)

    def debug_log(self, msg):
        """
        测试日志 不滚动 输出路径见 config.LOG_FILE
        :return:
        """
        logger = self.debug_logger()
        logger.info(msg)
