# -*- coding: utf-8 -*-
"""
@File: test_logger
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.logger.log import LogConfig, Log


if __name__ == '__main__':
    # ######  使用默认配置 #####
    Log().local_log("this is a log line use default config")

    # ####### 自定义配置 ######
    class CustomConfig(LogConfig):
        LOCAL_LOG_FILE = "/data/logs/custom_xxx.log"
        DEBUG_LOG_FILE = "/data/logs/debug_xxx.log"

    Log(CustomConfig).local_log("this is a log line use custom config")
