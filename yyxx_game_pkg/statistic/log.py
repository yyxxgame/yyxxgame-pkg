# -*- coding: utf-8 -*-
"""
@File: xlogging
@Author: ltw
@Time: 2024/1/5
"""
from yyxx_game_pkg.xlogging.log import LogMethods
from yyxx_game_pkg.xlogging.config import StatisticLogConfig


def logging_init():
    """
    配置logging
    注: 需在项目入口调用
    :return:
    """
    LogMethods.config(StatisticLogConfig)
