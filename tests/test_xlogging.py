# -*- coding: utf-8 -*-
"""
@File: test_xlogging
@Author: ltw
@Time: 2024/2/23
"""
import logging
from yyxx_game_pkg.xlogging.log import LogMethods
from yyxx_game_pkg.xlogging.config import StatisticLogConfig

LogMethods.config(StatisticLogConfig)


if __name__ == '__main__':
    # ######  使用默认配置 #####
    logging.debug("this is a debug log line use statistic config")
    logging.info("this is a info log line use default config")
    logging.error("this is a error log line use default config")
