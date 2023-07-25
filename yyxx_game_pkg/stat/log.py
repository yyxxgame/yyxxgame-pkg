# -*- coding: utf-8 -*-
"""
@File: log
@Author: ltw
@Time: 2023/3/10
@updateTime: 2023/07/24 by winslen
"""
# 未使用的也不能删除
from yyxx_game_pkg.logger.log import (
    LogLevelTyping,
    LogConfigTyping,
    root_log,
    Log,
    logger,
    local_logger,
    local_log,
    debug_logger,
    debug_log,
    LogConfig,
)


class StatLogConfig(LogConfig):
    """
    logging 配置
    """

    LOCAL_LOG_FILE = "/data/logs/local.log"
    DEBUG_LOG_FILE = "/data/logs/debug.log"


Log.init_config(StatLogConfig)
