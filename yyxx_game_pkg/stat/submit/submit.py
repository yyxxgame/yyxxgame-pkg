# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/15

from yyxx_game_pkg.stat.submit.logic.submit_logic import (
    to_protocol,
    process_proto,
    set_config,
    send,
)
from yyxx_game_pkg.logger.log import root_log


def submit_schedule(schedule: str, file_path: str, api_addr: str, jaeger: dict):
    # 配置
    set_config(file_path, api_addr)
    if jaeger:
        from yyxx_game_pkg.xtrace.helper import register_to_jaeger
        from opentelemetry.instrumentation.requests import RequestsInstrumentor

        RequestsInstrumentor().instrument()
        register_to_jaeger(**jaeger)

    # 构建schedule
    proto_list = []
    proto = to_protocol(schedule)
    if not proto:
        root_log(f"<submit_schedule> schedule is invalid, {schedule}, {file_path}")
        return None
    proto_list.extend(process_proto(proto))

    # 上报
    res_list = []
    for p in proto_list:
        res = send(p)
        res_list.append(res)

    return res_list
