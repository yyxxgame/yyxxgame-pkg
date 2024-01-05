# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/13
from celery import group
from ..core.structs import ProtoSchedule


class RuleBase:
    """
    RuleBase
    """

    def __init__(self):
        self._business_instance_name = None

    # region property
    @property
    def inst_name(self):
        """
        具体业务接口
        :return:
        """
        return self._business_instance_name

    @inst_name.setter
    def inst_name(self, val):
        self._business_instance_name = val

    # endregion

    # region 继承方法
    def build(self, schedule: ProtoSchedule):
        """
        构建独立的分发任务标签
        :return: [group, chord, chain, signature]
        """

    def make_signature_group(self, task_path, business_inst_name, queue, priority, kwargs_list=None):
        """
        构建单任务组
        :param task_path:
        :param business_inst_name:
        :param queue:
        :param priority:
        :param kwargs_list:
        :return:
        """
        sig_list = []
        if not kwargs_list:
            return None
        for kwargs in kwargs_list:
            _sig = self._make_signature(task_path, business_inst_name, **kwargs)
            _sig.options["queue"] = queue
            _sig.options["priority"] = priority
            sig_list.append(_sig)
        if not sig_list:
            return None
        sig = group(*sig_list)
        sig.options["queue"] = queue
        sig.options["priority"] = priority
        return sig

    @staticmethod
    def _make_signature(task_path, business_inst_name, *args, **kwargs):
        exec(f"from {task_path} import {business_inst_name}")
        return eval(business_inst_name).s(*args, **kwargs)

    # endregion
