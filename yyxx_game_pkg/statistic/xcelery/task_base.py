# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

"""
celery自定义任务基类
"""
import time
from abc import ABC

from celery import Task

from yyxx_game_pkg.stat.log import local_log


class TaskCustomBase(Task, ABC):
    """
    任务基类, 增加执行时间打印
    """

    def __init__(self):
        super().__init__()
        self._task_type = "TaskBase"
        self._start_time = 0

    @staticmethod
    def kwargs_logs(kwargs):
        """
        参数日志格式化
        :param kwargs:
        :return:
        """
        return str(kwargs)

    def before_start(self, task_id, args, kwargs):
        """
        before_start
        """
        self._start_time = time.time()
        kw_logs = self.kwargs_logs(kwargs)
        local_log(f"<{self._task_type}> before_start: {kw_logs}")

    def on_success(self, retval, task_id, args, kwargs):
        """
        on_success
        """
        end_time = time.time()
        kw_logs = self.kwargs_logs(kwargs)
        local_log(
            f"<{self._task_type}> on_success({end_time - self._start_time:.2f}s): {kw_logs}"
        )
        return super().on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        """
        on_failure
        :return:
        """
        end_time = time.time()
        local_log(
            f"<{self._task_type}> on_failure({end_time - self._start_time:.2f}s): "
            f"reason:{exc}, task_id:{task_id}, args:{args}, kwargs:{kwargs}"
        )
        return super().on_failure(exc, task_id, args, kwargs, einfo)


class QueryTaskCustomBase(TaskCustomBase):
    """
    QueryTaskCustomBase
    """

    def run(self, *args, **kwargs):
        pass

    def __init__(self):
        super().__init__()
        self._task_type = "QueryTaskTaskBase"

    @staticmethod
    def kwargs_logs(kwargs):
        """
        打印指定参数
        :param kwargs:
        :return:
        """
        schedule_name = kwargs.get("schedule_name")
        query_id = kwargs.get("query_id")
        query_name = kwargs.get("query_name")
        query_log_key = kwargs.get("query_log_key")
        server_id = kwargs.get("server_id")
        # 单服查询打印服ID
        server_id = server_id if query_log_key == "server_data" else ""
        return (
            f"schedule_name:{schedule_name}, "
            f"query_id:{query_id}({query_name}), "
            f"server_id: {server_id}, "
            f"sdate:{kwargs.get('sdate')}, edate:{kwargs.get('edate')}"
        )


class StatTaskCustomBase(TaskCustomBase):
    """
    StatTaskCustomBase
    """

    def run(self, *args, **kwargs):
        pass

    def __init__(self):
        super().__init__()
        self._task_type = "StatTaskTaskBase"

    @staticmethod
    def kwargs_logs(kwargs):
        """
        打印指定参数
        :param kwargs:
        :return:
        """
        schedule_name = kwargs.get("schedule_name")
        statistic_id = kwargs.get("statistic_id")
        ex_params = kwargs.get("ex_params")
        return (
            f"schedule_name:{schedule_name}, "
            f"statistic_id:{statistic_id}), "
            f"ex_params: {ex_params}, "
            f"sdate:{kwargs.get('sdate')}, edate:{kwargs.get('edate')}"
        )
