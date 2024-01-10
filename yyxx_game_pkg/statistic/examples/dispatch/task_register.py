# -*- coding: utf-8 -*-
"""
业务注册模块

@app.task(base=TaskCustomBase, ignore_result=True)      -> 注册celery的装饰器
def unique_function_name_instance(**kwargs):            -> 注册到celery的key（必须唯一）
    from business_class import function_instance        -> 业务入口路径
    return function_instance(**kwargs)                  -> 返回业务入口

"""
from celery import current_app as app
from yyxx_game_pkg.statistic.xcelery.task_base import TaskCustomBase
from yyxx_game_pkg.xtrace.helper import trace_span


# ######################## 统计服务接口 ###########################
@app.task(base=TaskCustomBase, ignore_result=True)
@trace_span(set_attributes=True)
def statistic_task_instance(*args, **kwargs):
    pass


@app.task(base=TaskCustomBase, ignore_result=True)
@trace_span()
def statistic_collect_instance(*args, **kwargs):
    pass


# ######################## 查询服务接口 ###########################
@app.task(base=TaskCustomBase, ignore_result=False)
@trace_span(set_attributes=True)
def query_task_instance(*args, **kwargs):
    pass


@app.task(base=TaskCustomBase, ignore_result=False)
@trace_span()
def query_collect_instance(*args, **kwargs):
    pass


# ######################## 捞数据服务接口 ###########################
@app.task(base=TaskCustomBase, ignore_result=False)
@trace_span(set_attributes=True)
def pull_task_instance(*args, **kwargs):
    pass


@app.task(base=TaskCustomBase, ignore_result=False)
@trace_span()
def pull_collect_instance(*args, **kwargs):
    pass


# ######################## 业务接口 ###########################
@app.task(base=TaskCustomBase, ignore_result=True)
@trace_span(set_attributes=True)
def crontab_task_instance(*args, **kwargs):
    pass


# ######################## 系统接口 ###########################
@app.task(base=TaskCustomBase, ignore_result=True)
def link_task(*_, **__):
    """
    连接任务
    详见:yyxx_game_pkg.statistic.dispatch.logic.workflows.WorkFlowMethods.link_task_s
    :param _:
    :param __:
    :return:
    """


# ######################## 测试接口 ###########################
@app.task(base=TaskCustomBase)
def add(*args, **kwargs):
    pass
