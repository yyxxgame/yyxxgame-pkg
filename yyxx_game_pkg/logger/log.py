# -*- coding: utf-8 -*-
"""
@File: log
@Author: ltw
@Time: 2023/2/6
@updateTime: 2023/07/24 by winslen
logger 默认设置
"""
import logging.config
import traceback
from typing import Literal, Type, TypeVar
from pathlib import Path

from .config import BaseLogConfig, LogConfig

# log日志级别
LogLevelTyping = Literal["critical", "error", "warning", "info", "debug"]

# LogConfig类及其子类
LogConfigTyping = TypeVar("LogConfigTyping", bound=BaseLogConfig)


def root_log(msg, level: LogLevelTyping = "warning", stacklevel: int = 2, addstacklevel=0):
    """
    root logger
    :param msg: 消息文本
    :param level: 消息级别
    :param stacklevel: 堆栈信息向上查找层数(默认2层,即为调用此函数的堆栈)
    :param addstacklevel: 以调用此函数的堆栈(stacklevel的值)作为基础,继续向上查找的层数,即stacklevel+addstacklevel层
    使用此参数无需关心下层函数的层级,只需要关心调用函数上层的层级即可
    """
    getattr(logging.getLogger(), level.lower())(msg, stacklevel=stacklevel+addstacklevel)


class Log:
    """
    singleton Log
    """

    _instance = None
    _init = False
    config = BaseLogConfig

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, log_config: Type[LogConfigTyping] = BaseLogConfig):
        if self._init or not log_config:
            return
        self._init = True
        # 日志配置初始化
        if not logging.getLogger().handlers:
            self.init_config(log_config)
        elif not self.config:
            self.config = BaseLogConfig

    @classmethod
    def init_config(cls, log_config: Type[LogConfigTyping] = LogConfig):
        """应用新配置"""
        self = cls()
        if log_config == self.config:
            return
        try:
            self.config = log_config
            self.make_path()
            logging.config.dictConfig(log_config.dict_config())
            root_log("logger init")
        except ValueError as _e:
            traceback.print_exc()

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
        try:
            for path in file_paths:
                path_obj = Path(path)
                path_obj.parent.mkdir(parents=True, exist_ok=True)
                path_obj.touch(exist_ok=True)
        except OSError as _e:
            traceback.print_exc()

    def root_logger(self) -> logging.Logger:
        """
        local_logger
        :return:
        """
        return logging.getLogger()

    def local_logger(self) -> logging.Logger:
        """
        local_logger
        :return:
        """
        return logging.getLogger(self.config.LOCAL_LOGGER_NAME)

    def debug_logger(self) -> logging.Logger:
        """
        debug_logger
        :return:
        """
        return logging.getLogger(self.config.DEBUG_LOGGER_NAME)

    def local_log(self, msg: str, level: LogLevelTyping = "info", stacklevel: int = 2, addstacklevel=0, **kwargs):
        """
        正常滚动日志 输出路径见 config.LOG_FILE
        :param msg: 消息文本
        :param level: 消息级别
        :param stacklevel: 堆栈信息向上查找层数(默认2层,即为调用此函数的堆栈)
        :param addstacklevel: 以调用此函数的堆栈(stacklevel的值)作为基础,继续向上查找的层数,即stacklevel+addstacklevel层
            使用此参数无需关心下层函数的层级,只需要关心调用函数上层的层级即可
        :param kwargs: 额外参数
        :return:
        """
        if kwargs:
            self.root_logger().warning(f"[yyxx-Log] Unexpected parameters => {kwargs}")
        getattr(self.local_logger(), level.lower())(msg, stacklevel=stacklevel+addstacklevel)

    def debug_log(self, msg: str, level: LogLevelTyping = "info", stacklevel: int = 2, addstacklevel=0, **kwargs):
        """
        测试日志 不滚动 输出路径见 config.LOG_FILE
        :param msg: 消息文本
        :param level: 消息级别
        :param stacklevel: 堆栈信息向上查找层数(默认2层,即为调用此函数的堆栈)
        :param addstacklevel: 以调用此函数的堆栈(stacklevel的值)作为基础,继续向上查找的层数,即stacklevel+addstacklevel层
            使用此参数无需关心下层函数的层级,只需要关心调用函数上层的层级即可
        :param kwargs: 额外参数
        :return:
        """
        if kwargs:
            self.root_logger().warning(f"[yyxx-Log] Unexpected parameters => {kwargs}")
        getattr(self.debug_logger(), level.lower())(msg, stacklevel=stacklevel + addstacklevel)


logger = Log()
local_logger = logger.local_logger()
local_log = logger.local_log
debug_logger = logger.debug_logger()
debug_log = logger.debug_log
