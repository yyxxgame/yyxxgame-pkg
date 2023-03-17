# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14
from yyxx_game_pkg.stat.dispatch.common.log import local_log
from yyxx_game_pkg.stat.dispatch.core.manager import rule_register
from yyxx_game_pkg.stat.dispatch.core.workflows import WorkFlowMethods
from yyxx_game_pkg.stat.dispatch.logic.task_logic import parse_task
from yyxx_game_pkg.stat.dispatch.rules.rule_base import RuleBase


@rule_register(inst_name_list=["work_flow_instance"])
class DispatchRuleWorkFlow(RuleBase):
    def __init__(self):
        super(self.__class__, self).__init__()

    # region 继承方法
    def build(self, schedule):
        """
        构建分发任务标签
        :return: [group, chord, chain, signature]
        """
        return self.__logic_make_sig(schedule)

    # endregion

    # region 内部方法
    def __logic_make_sig(self, schedule):
        flow_content_dict = schedule.SCHEDULE_CONTENT
        assert isinstance(flow_content_dict, dict)
        sig_list = []
        for _, flow_content in flow_content_dict.items():
            sig = self.__make_sig_by_content(schedule, flow_content)
            if not sig:
                continue
            sig_list.append(sig)

        return sig_list

    def __parse_flow_content(self, flow_content):
        assert isinstance(flow_content, dict)
        dict_step_sig_list = dict()
        min_step = 65535
        max_step = -1
        for step, content_list in flow_content.items():
            step = int(step)
            min_step = min(step, min_step)
            max_step = max(step, max_step)
            for schedule_str in content_list:
                if schedule_str == self.inst_name:
                    # 工作流的子计划中不能再包含工作流
                    local_log(
                        "[ERROR] <DispatchRuleWorkFlow> __parse_flow_content, "
                        "workflow can not contain workflow, schedule:{}".format(
                            schedule_str
                        )
                    )
                    return None, -1, -1

                sub_sig_list = parse_task(schedule_str)
                if not sub_sig_list:
                    # 不能跳过sig
                    local_log(
                        "[ERROR] <DispatchRuleWorkFlow> __parse_flow_content, "
                        "parse_schedule_str_to_signature, schedule:{}".format(
                            schedule_str
                        )
                    )
                    return None, -1, -1

                if not dict_step_sig_list.get(step):
                    dict_step_sig_list[step] = []
                if isinstance(sub_sig_list, list):
                    dict_step_sig_list[step].extend(sub_sig_list)
                else:
                    dict_step_sig_list[step].append(sub_sig_list)

        return dict_step_sig_list, min_step, max_step

    def __make_sig_by_content(self, schedule, flow_content):
        dict_step_sig_list, min_step, max_step = self.__parse_flow_content(flow_content)
        if dict_step_sig_list is None:
            local_log(
                "[ERROR] <DispatchRuleWorkFlow>dict_step_sig_list is None, content:{}".format(
                    flow_content
                )
            )
            return None
        queue_name = dict_step_sig_list[min_step][0].options.get("queue")

        # step合并
        step_sig_list = []
        for step in range(min_step, max_step + 1):
            # 按照step先后顺序构建sig列表
            sig_list = dict_step_sig_list.get(step)
            if not sig_list:
                continue
            res_sig = WorkFlowMethods.merge_sig_list(sig_list)  # 多个相同同step的sig合并
            step_sig_list.append(res_sig)

        # 构建chord
        ch = WorkFlowMethods.link_signatures(step_sig_list)
        if ch is None:
            local_log(
                "[ERROR] <DispatchRuleWorkFlow>__make_sig_by_content, make chord error, content:{}".format(
                    flow_content
                )
            )
        else:
            local_log(
                "<DispatchRuleWorkFlow>__make_sig_by_content, queue:{} steps:{}".format(
                    queue_name, max_step
                )
            )
        return ch

    # endregion
