# -*- coding: utf-8 -*-
"""
@File: rule_statistic_multi_flow
@Author: ltw
@Time: 2024/1/3
"""
from ..core.manager import rule_register
from .rule_statistic_flow import RuleStatisticFlowLogic


class RuleStatisticMultiFlowLogic(RuleStatisticFlowLogic):
    """
    RuleStatisticMultiFlowLogic
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
        sig = self.traversal_build(schedule, self.build_workflow_sig_logic, ignore_result=True)
        return sig


@rule_register(
    inst_name_list=[
        "multiple_workflow_instance",
        "statistic_multi_flow_instance",
    ]
)
class RuleStatisticMultiFlow(RuleStatisticMultiFlowLogic):
    """
    RuleStatisticMultiFlow
    """
