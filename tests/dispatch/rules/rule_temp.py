# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/13
from yyxx_game_pkg.stat.dispatch.core.manager import rule_register, RuleManager
from yyxx_game_pkg.stat.dispatch.core.structs import ProtoSchedule
from yyxx_game_pkg.stat.dispatch.core.workflows import WorkFlowMethods
from yyxx_game_pkg.stat.dispatch.rules.rule_base import RuleBase
from celery import current_app as app


@rule_register(
    inst_name_list=["temp_task_instance", "add", "function_test_instance", "gather"]
)
class RuleTemp(RuleBase):
    def __init__(self):
        super().__init__()

    def build(self, schedule: ProtoSchedule):
        content = schedule.SCHEDULE_CONTENT
        queue = schedule.SCHEDULE_QUEUE_NAME
        print(f"<RuleTemp> content:{content}")

        sig_list = []
        for content in schedule.SCHEDULE_CONTENT:
            kwargs_list = []
            if content.get("kwargs_list"):
                k_l = content["kwargs_list"]
                for k in k_l:
                    kwargs_list.append(k)

            sig = WorkFlowMethods.make_signature_batch(
                app.conf.get("CUSTOM_TASK_REGISTER_PATH"),
                self.inst_name,
                kwargs_list,
                queue_name=queue,
            )
            sig_list.append(sig)

        s = WorkFlowMethods.link_signatures(sig_list)
        return s
