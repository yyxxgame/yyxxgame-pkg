# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/10/08 11:09:01
# @Software : python3.11
# @Desc     : TODO
import json
from functools import wraps

from flask import g
from opentelemetry import trace

from yyxx_game_pkg.crypto.aes import encryption_deal_with


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
