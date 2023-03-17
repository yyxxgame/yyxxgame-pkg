# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/8
from opentelemetry.instrumentation.requests import RequestsInstrumentor

# test
# init request
from yyxx_game_pkg.xtrace.helper import register_to_jaeger, trace_span

RequestsInstrumentor().instrument()

# jaeger
register_to_jaeger("test-xtrace", "jaeger-host")


@trace_span()
def process():
    ret_value = "success"
    print("this is a process func")
    return ret_value


@trace_span(ret_trace_id=True)
def process_with_trace_id():
    ret_value = "success"
    print("this is a process with trace id func")
    return ret_value


@trace_span(set_attributes=True)
def func_business_on_set_attributes(**kwargs):
    ret_value = "success"
    print("this is a process on set jaeger tags")
    return ret_value


if __name__ == "__main__":
    res = process()
    print(res)

    res, trace_id = process_with_trace_id()
    print("res: {}".format(res) + " trace_id: {}".format(trace_id))
