# -*- coding: utf-8 -*-
# @Author   : LvWenQi
# @Time     : 2023/07/05

import logging.handlers
from django.conf import settings

from yyxx_game_pkg.xtrace.helper import get_current_trace_id


class TraceFormatter(logging.Formatter):
    def format(self, record):
        # 获取当前的日志消息
        msg = record.getMessage()
        trace_id = get_current_trace_id()[2:]
        if getattr(settings, "JAEGER_UI_URL", None):
            trace_id = f"http://{settings.JAEGER_UI_URL}/trace/{trace_id}"
        # 根据当前的日志消息动态生成写入logger的消息
        return (
            f"""[{self.formatTime(record)}] [pid:{record.process}] [{record.filename} {record.module} """
            f"""{record.funcName}:{record.lineno}] [{record.name}:{record.levelname}] - ["trace":"{trace_id}"] {msg}"""
        )