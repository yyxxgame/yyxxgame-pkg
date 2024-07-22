# -*- coding: utf-8 -*-
"""
@File: rule_statistic_flow
@Author: ltw
@Time: 2023/12/28
"""

from celery import chain, chord

from ..core.manager import rule_register
from ..logic.workflows import WorkFlowMethods as Flow
from .rule_statistic_task import RuleStatisticTaskLogic
from .rule_base import ProtoSchedule


class RuleStatisticFlowLogic(RuleStatisticTaskLogic):
    """
    RuleStatisticFlowLogic
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
    def traversal_build(schedule, sub_sig_build_fn, ignore_result=None):
        """
        循环构建子任务
        :param schedule:
        :param sub_sig_build_fn:
        :param ignore_result:  不需要上一步的结果
        :return:
        """
        sig_options = {"queue": schedule.queue, "priority": schedule.priority}
        # 汇总所有group和step
        groups_sigs = {}
        for group, _group_contents in schedule.schedule_content.items():
            step_keys = sorted(list(map(int, _group_contents.keys())))
            group_sigs = {}
            for step in step_keys:
                if step not in group_sigs:
                    group_sigs[step] = {"sigs": [], "chord": False}
                _step_contents = _group_contents[str(step)]
                _step_sigs = []
                for _schedule in _step_contents:
                    _proto = ProtoSchedule(_schedule)
                    _sig = sub_sig_build_fn(_proto)
                    if not _sig:
                        continue
                    # todo 配置项
                    # 暂时用 collect 判断是否依赖结果
                    use_chord = (
                        _proto.schedule_dispatch_rule_instance_name.find("collect") >= 0
                    )
                    use_chord = (
                        (not ignore_result) if ignore_result is not None else use_chord
                    )
                    # 所有group第一步不使用chord
                    if step_keys.index(step) == 0:
                        use_chord = False
                    group_sigs[step]["chord"] = use_chord
                    group_sigs[step]["sigs"].append(_sig)
            groups_sigs[group] = group_sigs

        steps_sig_list = []

        for group, _group_sigs in groups_sigs.items():
            for step in sorted(list(map(int, _group_sigs.keys()))):
                _step_sigs = _group_sigs[step]["sigs"]
                # 有依赖任务 该步骤用chord
                if _group_sigs[step]["chord"]:
                    steps_sig_list.append(
                        chord(_step_sigs, Flow.link_task_s(**sig_options))
                    )
                else:
                    steps_sig_list.append(chain(*_step_sigs))

        if not steps_sig_list:
            return None
        sig = chain(*steps_sig_list)
        sig.options.update(sig_options)
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


@rule_register(inst_name_list=["work_flow_instance", "statistic_flow_instance"])
class RuleStatisticFlow(RuleStatisticFlowLogic):
    """
    RuleStatisticFlow
    """
