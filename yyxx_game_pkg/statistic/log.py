# -*- coding: utf-8 -*-
"""
@File: xlogging
@Author: ltw
@Time: 2024/1/5
"""
import logging
from yyxx_game_pkg.xlogging.log import LogMethods
from yyxx_game_pkg.xlogging.config import StatisticLogConfig


def logging_init():
    """
    配置logging
    注: 需在项目入口调用
    :return:
    """
    LogMethods.config(StatisticLogConfig)


def local_log(msg):
    """
    旧local_log兼容处理
    """
    logging.info(msg)


def debug_log(msg):
    """
    旧debug_log兼容处理
    """
    logging.debug(msg)
