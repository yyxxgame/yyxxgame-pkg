# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2023/6/13
"""
import os
import logging.handlers
from yyxx_game_pkg.xtrace.helper import get_current_trace_id


class TraceFormatter(logging.Formatter):
    # JAEGER UI trace地址
    JAEGER_WEB_URL = ""
    # 打入url的日志LEVEL
    JAEGER_WEB_URL_LEVELS = []

    def format(self, record):
        # 获取当前的日志消息
        if not self.JAEGER_WEB_URL:
            self.JAEGER_WEB_URL = os.environ.get("JAEGER_WEB_URL", "")
            self.JAEGER_WEB_URL_LEVELS = os.environ.get("JAEGER_WEB_URL_LEVELS", "").upper()
        record.jaeger_web_url = self.JAEGER_WEB_URL
        record.trace_url = record.trace_id = get_current_trace_id()[2:]
        if record.trace_id != "0" and (
            not self.JAEGER_WEB_URL_LEVELS or record.levelname in self.JAEGER_WEB_URL_LEVELS
        ):
            record.trace_url = f"{record.jaeger_web_url}{record.trace_id}"
        return super().format(record)
