# -*- coding: utf-8 -*-
"""
@File: log
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.logger import log
from yyxx_game_pkg.xtrace.helper import get_current_trace_id


class StatLogConfig(log.LogConfig):
    """
    logging 配置
    """
    LOCAL_LOG_FILE = "/data/logs/local.log"
    DEBUG_LOG_FILE = "/data/logs/debug.log"


logger = log.Log(StatLogConfig)


def local_log(msg):
    """
    local log rotate file
    :param msg:
    :return:
    """
    trace_id = get_current_trace_id()
    msg = f"[{trace_id}] {msg}"
    logger.local_log(msg)


def debug_log(msg):
    """
    debug log file
    :param msg:
    :return:
    """
    logger.debug_log(msg)
