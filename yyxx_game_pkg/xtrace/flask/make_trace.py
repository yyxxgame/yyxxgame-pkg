# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/08/14 14:23:05
# @Software : python3.11
# @Desc     : TODO
import json
from functools import wraps

from flask import g
from opentelemetry import trace

from yyxx_game_pkg.crypto.aes import encryption_deal_with


def make_trace_parent():
    span = trace.get_current_span()
    span_context = span.get_span_context()
    if span_context == trace.INVALID_SPAN_CONTEXT:
        return {}
    trace_id = trace.format_trace_id(span_context.trace_id)
    trace_parent_string = f"00-{trace_id}-{trace.format_span_id(span_context.span_id)}-{span_context.trace_flags:02x}"
    return {
        "trace_id": trace_id,
        "trace_parent_string": trace_parent_string,
    }


def trace_request(func):
    @wraps(func)
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        g.request_params = kwargs
        return res
    return inner


def trace_response(func):
    @wraps(func)
    def inner(self, data):
        temp = self.whether_decryption
        self.whether_decryption = False
        response_data_raw = func(self, data)
        response_data = json.loads(response_data_raw)
        if isinstance(response_data, dict):
            trace_info = make_trace_parent()
            response_data["trace"] = trace_info
            g.response_params = response_data
            response_data = json.dumps(response_data)
            if temp:
                response_data = encryption_deal_with(response_data, "E")
            return response_data
        else:
            return response_data_raw
    return inner