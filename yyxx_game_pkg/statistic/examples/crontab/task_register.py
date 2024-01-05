# -*- coding: utf-8 -*-
"""
业务注册模块

@app.task(base=TaskCustomBase, ignore_result=True)      -> 注册celery的装饰器
def unique_function_name_instance(**kwargs):            -> 注册到celery的key（必须唯一）
    from business_class import function_instance        -> 业务入口路径
    return function_instance(**kwargs)                  -> 返回业务入口

"""
import logging
import subprocess
from celery import current_app as app
from yyxx_game_pkg.statistic.xcelery.task_base import TaskCustomBase
from yyxx_game_pkg.xtrace.helper import trace_span


@app.task(base=TaskCustomBase, ignore_result=True)
@trace_span(set_attributes=True)
def crontab_task_instance(*_, **kwargs):
    """
    定时任务
    :param _:
    :param kwargs:
    :return:
    """
    cmd = kwargs["cmd"]
    # cmd = "python --version"
    output_str = subprocess.getstatusoutput(cmd)
    logging.info("crontab_task_instance cmd:%s, res:%s", cmd, output_str)
