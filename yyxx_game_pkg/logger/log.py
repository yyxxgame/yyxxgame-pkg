# -*- coding: utf-8 -*-
"""
@File: log
@Author: ltw
@Time: 2023/2/6
"""
import logging.config
from datetime import datetime
from .config import LogConfig


def local_log(msg):
    Log().local_log(msg)


def debug_log(msg):
    Log().debug_log(msg)


class Log:
    _instance = None
    _init = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_config=LogConfig):
        if self._init:
            return
        # 日志配置初始化
        self.config = log_config
        logging.config.dictConfig(self.config.config())
        self.local_log("logger init")

    def local_logger(self):
        """
        local_logger
        :return:
        """
        return logging.getLogger(self.config.local_logger_name())

    def debug_logger(self):
        """
        debug_logger
        :return:
        """
        return logging.getLogger(self.config.debug_logger_name())

    def local_log(self, msg):
        """
        正常滚动日志 输出路径见 config.LOG_FILE
        :return:
        """
        logger = self.local_logger()
        now = datetime.now()
        # info = {
        #     "@timestamp": str(now),
        #     "msg": msg
        # }
        # logger.info(info)
        msg = f"[{now}] {msg}"
        logger.info(msg)

    def debug_log(self, msg):
        """
        测试日志 不滚动 输出路径见 config.LOG_FILE
        :return:
        """
        logger = self.debug_logger()
        logger.info(msg)
