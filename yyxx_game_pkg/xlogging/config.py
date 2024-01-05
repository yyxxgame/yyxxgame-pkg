# -*- coding: utf-8 -*-
"""
log config
"""


class LogConfig:
    """
    LogConfig
    不同项目配置调整继承该类
    """

    @classmethod
    def dict_config(cls):
        """
        logging dictConfig
        :return:
        """
        return {}


class StatisticLogConfig(LogConfig):
    """
    后台统计用配置
    """

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
                    "class": "yyxx_game_pkg.xlogging.formatters.TraceFormatter",
                    "format": (
                        "[%(asctime)s,%(msecs)d: %(levelname)s/%(process)d][%(filename)s:%(funcName)s:%(lineno)d]"
                        '["trace":"%(trace_id)s"] %(message)s'
                    ),
                },
            },
            "handlers": {
                "rotate_file_handler": {
                    "level": "INFO",
                    "formatter": "def_fmt",
                    "class": "yyxx_game_pkg.xlogging.handlers.MultiProcessTimedRotatingFileHandler",
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
                    "level": "DEBUG",
                    "formatter": "def_fmt",
                    "class": "logging.StreamHandler",
                },
            },
            # 接收DEBUG级日志 传递至handlers, 通过handlers配置对不同级别日志进行分别处理
            "loggers": {
                "": {  # root logger
                    "handlers": ["rotate_file_handler", "debug_file_handler", "console_handler"],
                    "level": "DEBUG",
                    "propagate": True,
                },
            },
        }
        return log_config
