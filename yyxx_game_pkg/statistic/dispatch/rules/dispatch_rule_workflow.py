# -*- coding: utf-8 -*-
"""
@File: dispatch_rule_workflow
@Author: ltw
@Time: 2023/12/28
"""
from celery import chain, group

from ..core.manager import rule_register
from .dispatch_rule_statistic_task import DispatchRuleStatisticTaskLogic
from .rule_base import ProtoSchedule


class DispatchRuleWorkFlowLogic(DispatchRuleStatisticTaskLogic):
    """
    DispatchRuleWorkFlow
    """

    # region 继承方法
    def build(self, schedule):
        """
        构建分发任务标签
        :return: [group, chord, chain, signature]
        """
        sig = self.build_workflow_sig_logic(schedule)
        return sig

    # endregion

    @staticmethod
    def traversal_build(schedule, sub_sig_build_fn):
        """
        循环构建子任务
        :param schedule:
        :param sub_sig_build_fn:
        :return:
        """
        content_dict = schedule.schedule_content
        steps_contents = {}
        for _, _content in content_dict.items():
            for step, content_list in _content.items():
                steps_contents[int(step)] = content_list
        step_keys = list(steps_contents.keys())
        step_keys = sorted(step_keys)
        steps_sig_list = []
        for step in step_keys:
            _step_contents = steps_contents[step]
            if not _step_contents:
                continue
            _step_sigs = []
            for _schedule in _step_contents:
                _proto = ProtoSchedule(_schedule)
                sub_sig = sub_sig_build_fn(_proto)
                if not sub_sig:
                    continue
                _step_sigs.append(sub_sig)
            if not _step_sigs:
                continue
            steps_sig_list.append(group(*_step_sigs))
        if not steps_sig_list:
            return None
        sig = chain(*steps_sig_list)
        sig.options["queue"] = schedule.queue
        sig.options["priority"] = schedule.priority
        return sig

    def build_workflow_sig_logic(self, schedule):
        """
        构建单工作流(多任务)
        :param schedule:
        :return:
        """
        content_dict = schedule.schedule_content
        assert isinstance(content_dict, dict)
        sig = self.traversal_build(schedule, self.build_sig_logic)
        return sig


@rule_register(
    inst_name_list=[
        "work_flow_instance",
    ]
)
class DispatchRuleWorkFlow(DispatchRuleWorkFlowLogic):
    """
    DispatchRuleWorkFlow
    """
