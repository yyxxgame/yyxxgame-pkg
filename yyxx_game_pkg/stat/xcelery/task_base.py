# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

"""
celery自定义任务基类
"""

from celery import Task


class TaskCustomBase(Task):
    def __init__(self):
        self._task_type = "TaskBase"

    def on_success(self, retval, task_id, args, kwargs):
        print(
            f'<{ self._task_type}> on_success: {task_id}, kwargs:{kwargs.get("schedule_name")}, '
            f'statistic_id:{kwargs.get("statistic_id")}, svr_id_slice_size:{len(kwargs.get("server_ids", [])),}, '
            f'sdate:{kwargs.get("sdate")}, edate:{kwargs.get("edate")}'
        )
        return super(TaskCustomBase, self).on_success(retval, task_id, args, kwargs)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print(
            f"<{self._task_type}> on_failure, reason:{exc}, task_id:{task_id}, args:{args}, kwargs:{kwargs}"
        )
        return super(TaskCustomBase, self).on_failure(exc, task_id, args, kwargs, einfo)
