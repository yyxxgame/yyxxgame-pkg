# -*- coding: utf-8 -*-
"""
@File: rule_statistic_flow
@Author: ltw
@Time: 2023/12/28
"""

from celery import chain, chord, group

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
        for _group, _group_contents in schedule.schedule_content.items():
            if not _group_contents.keys():
                continue
            step_keys = sorted(list(map(int, _group_contents.keys())))
            group_sigs = {}
            for step in step_keys:
                if step not in group_sigs:
                    group_sigs[step] = {"sigs": [], "chord": False}
                if step in _group_contents:
                    _step_contents = _group_contents[step]
                elif str(step) in _group_contents:
                    _step_contents = _group_contents[str(step)]
                else:
                    continue
                for _schedule in _step_contents:
                    _proto = ProtoSchedule(_schedule)
                    _sig = sub_sig_build_fn(_proto)
                    if not _sig:
                        continue
                    # 当前step是否需要结果由(step + 1)任务处理
                    group_sigs[step]["chord"] = False

                    need_result = (
                        _proto.schedule_dispatch_rule_instance_name.find("collect") >= 0
                    )

                    immut = _proto.schedule_content.get("immutable", 0)
                    if immut:
                        need_result = False

                    last_chord = (
                        (not ignore_result)
                        if ignore_result is not None
                        else need_result
                    )
                    if last_chord and ((step - 1) in group_sigs):
                        group_sigs[step - 1]["chord"] = True

                    group_sigs[step]["chord"] = need_result
                    group_sigs[step]["sigs"].append(_sig)
            groups_sigs[_group] = group_sigs

        steps_sig_list = []

        for _group, _group_sigs in groups_sigs.items():
            for step in sorted(list(_group_sigs.keys())):
                _step_sigs = _group_sigs[step]["sigs"]

                if _group_sigs[step]["chord"]:
                    # 有依赖任务
                    steps_sig_list.append(
                        chord(_step_sigs, Flow.link_task_s(**sig_options))
                    )
                else:
                    # 无依赖任务 忽略结果
                    steps_sig_list.append(
                        group(
                            *_step_sigs
                        )
                    )

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
