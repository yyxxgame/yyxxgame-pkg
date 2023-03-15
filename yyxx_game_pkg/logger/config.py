# -*- coding: utf-8 -*-
"""
log config
"""


class LogConfig:
    """
    log config class
    不同项目配置调整继承该类
    """

    DEBUG_LOGGER_NAME = "py_debug"
    LOCAL_LOGGER_NAME = "py_local"

    LOCAL_LOG_FILE = "/tmp/local.log"
    DEBUG_LOG_FILE = "/tmp/debug.log"

    @classmethod
    def dict_config(cls):
        """
        LOG_CONFIG DICT
        """
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "def_fmt": {
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "[%(asctime)s,%(msecs)d: %(levelname)s/%(process)d] %(message)s",
                    "class": "logging.Formatter",
                },
            },
            "handlers": {
                "rotate_file_handler": {
                    "level": "INFO",
                    "formatter": "def_fmt",
                    "class": "yyxx_game_pkg.logger.handlers.MultiProcessTimedRotatingFileHandler",
                    "filename": cls.LOCAL_LOG_FILE,
                    "when": "MIDNIGHT",
                    "backupCount": 7,
                },
                "debug_file_handler": {
                    "level": "DEBUG",
                    "formatter": "def_fmt",
                    "class": "logging.FileHandler",
                    "filename": cls.DEBUG_LOG_FILE,
                },
                "console_handler": {
                    "level": "INFO",
                    "formatter": "def_fmt",
                    "class": "logging.StreamHandler",
                },
            },
            "loggers": {
                "": {  # root logger
                    "handlers": ["rotate_file_handler", "console_handler"],
                    "level": "WARNING",
                    "propagate": False,
                },
                cls.LOCAL_LOGGER_NAME: {
                    "handlers": ["rotate_file_handler", "console_handler"],
                    "level": "INFO",
                    "propagate": False,
                },
                cls.DEBUG_LOGGER_NAME: {
                    "handlers": ["debug_file_handler", "console_handler"],
                    "level": "DEBUG",
                    "propagate": False,
                },
            },
        }
        return log_config
