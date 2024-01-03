# -*- coding: utf-8 -*-
"""
@File: dispatch_rule_multi_workflow
@Author: ltw
@Time: 2024/1/3
"""
from ..core.manager import rule_register
from .dispatch_rule_workflow import DispatchRuleWorkFlowLogic


class DispatchRuleMultipleWorkFlowLogic(DispatchRuleWorkFlowLogic):
    """
    RuleMultiWorkFlow
    """

    # region 继承方法
    def build(self, schedule):
        """
        构建分发任务标签
        :return: [group, chord, chain, signature]
        """
        sig = self.build_multi_workflow_sig_logic(schedule)
        return sig

    # endregion

    def build_multi_workflow_sig_logic(self, schedule):
        """
        构建多步骤工作流任务
        :param schedule:
        :return:
        """
        content_dict = schedule.schedule_content
        assert isinstance(content_dict, dict)
        sig = self.traversal_build(schedule, self.build_workflow_sig_logic)
        return sig


@rule_register(
    inst_name_list=[
        "multiple_workflow_instance",
    ]
)
class DispatchRuleMultipleWorkFlow(DispatchRuleMultipleWorkFlowLogic):
    """
    DispatchRuleMultiWorkFlow
    """
