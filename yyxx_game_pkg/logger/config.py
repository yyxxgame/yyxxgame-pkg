# -*- coding: utf-8 -*-
"""
log config
"""


class LogConfig:
    """
    log config class
    不同项目配置调整继承该类
    """

    @staticmethod
    def debug_logger_name():
        """
        debug logger name
        """
        return "py_debug"

    @staticmethod
    def local_logger_name():
        """
        local logger name
        """
        return "py_local"

    @staticmethod
    def local_log_file():
        """
        local log file path
        """
        return "/data/logs/local.log"

    @staticmethod
    def debug_log_file():
        """
        debug log file path
        """
        return "/data/logs/debug.log"

    @staticmethod
    def config():
        """
        LOG_CONFIG DICT
        """
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "def_fmt": {
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s %(levelname)-8s: %(message)s",
                    "class": "logging.Formatter",
                },
            },
            "handlers": {
                "rotate_file_handler": {
                    "level": "INFO",
                    "formatter": "def_fmt",
                    "class": "public.logger.handlers.MultiProcessTimeRotatingFileHandler",
                    "filename": LogConfig.local_log_file(),
                    "when": "MIDNIGHT",
                    "backupCount": 7,
                },
                "debug_file_handler": {
                    "level": "DEBUG",
                    "formatter": "def_fmt",
                    "class": "logging.FileHandler",
                    "filename": LogConfig.debug_log_file(),
                },
                "console_handler": {
                    "level": "INFO",
                    "formatter": "def_fmt",
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                LogConfig.debug_logger_name(): {
                    "handlers": ["debug_file_handler", "console_handler"],
                    "level": "DEBUG",
                    "propagate": False,
                },
                LogConfig.local_logger_name(): {
                    "handlers": ["rotate_file_handler", "console_handler"],
                    "level": "INFO",
                    "propagate": False,
                },
            },
        }
        return log_config
