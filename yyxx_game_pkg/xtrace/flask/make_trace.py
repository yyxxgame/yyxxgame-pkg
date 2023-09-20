# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/08/14 14:23:05
# @Software : python3.6
# @Desc     : flask trace
import json
from functools import wraps

from flask import g
from opentelemetry import trace

from yyxx_game_pkg.crypto.aes import encryption_deal_with


def make_trace_parent():
    span = trace.get_current_span()
    span_context = span.get_span_context()
    if span_context == trace.INVALID_SPAN_CONTEXT:
        return ""
    trace_id = trace.format_trace_id(span_context.trace_id)
    trace_parent_string = f"00-{trace_id}-{trace.format_span_id(span_context.span_id)}-{span_context.trace_flags:02x}"
    return trace_parent_string


def trace_request(func):
    @wraps(func)
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        kwargs.get("data_list", {}).pop("ch_conter", None)
        g.request_params = json.dumps(kwargs)
        return res

    return inner


def trace_response(func):
    @wraps(func)
    def inner(self, data):
        temp = self.whether_decryption
        self.whether_decryption = False
        response_data_raw = func(self, data)
        g.response_params = response_data_raw
        if temp:
            response_data_raw = encryption_deal_with(response_data_raw, "E")
        return response_data_raw

    return inner


def set_trace_tags(params=(), action=""):
    def decorator(func):
        @wraps(func)
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            span = trace.get_current_span()
            attributes = {k: kwargs.get(k, None) for k in params}
            attributes["action"] = action
            span.set_attributes(attributes)
            return res

        return inner

    return decorator
