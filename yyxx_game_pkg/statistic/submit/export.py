# -*- coding: utf-8 -*-
"""
@File: export
@Author: ltw
@Time: 2024/1/2
"""

from .logic import (
    process_schedule,
    set_config,
    send,
)


def submit_schedule(schedule: str, file_path: str, api_addr: str, jaeger: dict):
    # 配置
    set_config(file_path, api_addr)
    if jaeger:
        from yyxx_game_pkg.xtrace.helper import register_to_jaeger
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        RequestsInstrumentor().instrument()
        register_to_jaeger(**jaeger)

    # 构建proto_dict
    proto_dict = process_schedule(schedule)
    res = send(proto_dict)
    return res
