# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2024/04/16
"""
from ..core.manager import rule_register
from .rule_statistic_flow import RuleStatisticFlowLogic
from .rule_query_task import RuleQueryTaskLogic


class RuleQueryFlowLogic(RuleQueryTaskLogic, RuleStatisticFlowLogic):
    """
    RuleQueryFlowLogic
    """

    def build(self, schedule):
        """
        构建分发任务标签
        :return: [group, chord, chain, signature]
        """
        sig = self.build_workflow_sig_logic(schedule)
        return sig

    # region 继承方法
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
        "query_work_flow_instance",
        "query_flow_instance",
    ]
)
class RuleQueryFlow(RuleQueryFlowLogic):
    """
    RuleQueryFlow
    """
