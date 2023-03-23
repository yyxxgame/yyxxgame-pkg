# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14
from celery import current_app as app
from yyxx_game_pkg.stat.xcelery.task_base import TaskCustomBase
from yyxx_game_pkg.xtrace.helper import trace_span


@app.task(base=TaskCustomBase, ignore_result=True)
@trace_span(set_attributes=True)
def add(x, y):
    print("add:", x, y)
    return x + y


@app.task(base=TaskCustomBase, ignore_result=True)
@trace_span(set_attributes=True)
def gather(*args, **kwargs):
    l = len(args)
    print("gather:", l, args)
    return [l, args]


@app.task(base=TaskCustomBase, ignore_result=True)
def function_test_instance(*args, **kwargs):
    l = len(args)
    print("function_test_instance", l, args, kwargs)
    return [l, args, kwargs]
