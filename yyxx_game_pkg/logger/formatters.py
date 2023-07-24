# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2023/6/13
"""

import logging.handlers
from yyxx_game_pkg.xtrace.helper import get_current_trace_id


class TraceFormatter(logging.Formatter):
    def format(self, record):
        # 获取当前的日志消息
        record.trace_id = get_current_trace_id()
        return super().format(record)
