# -*- coding: utf-8 -*-
"""
@File: test_submit_schedule
@Author: ltw
@Time: 2024/7/19

test_submit 目录下执行 pytest
"""

import pytest
import json

from yyxx_game_pkg.statistic.submit.logic import process_schedule, set_config
from yyxx_game_pkg.statistic.submit.export import submit_schedule


@pytest.mark.parametrize(
    "schedule",
    [
        "schedule_test_statistic_task@schedule_tests",
        "schedule_test_statistic_flow@schedule_tests",
        "schedule_test_statistic_multi_flow@schedule_tests",
        # "schedule_test_query_task@schedule_test",
        # "schedule_test_query_flow@schedule_test",
    ],
)
class TestProcessSchedule:
    """
    process_schedule 单元测试
    """

    # TODO query ltw

    def test_send(self, schedule):
        """
        :param schedule:
        :return:
        """
        from yyxx_game_pkg.statistic.dispatch.logic.task_logic import parse_task
        from yyxx_game_pkg.statistic.dispatch.rules import (
            rule_statistic_task,
            rule_statistic_flow,
            rule_statistic_multi_flow,
        )

        set_config(path="tests.test_submit.schedule_rule", api_addr="")
        proto_dict = process_schedule(schedule)
        sig = parse_task(proto_dict)
        assert sig != []

    def test_submit(self, schedule):
        """
        :param schedule:
        :return:
        (需起dispatch)
        """
        conf_path = "test_submit.json"
        with open(conf_path, "r", encoding="utf8") as f:
            conf = json.load(f)
        res = submit_schedule(
            schedule,
            conf["register_path"],
            conf["dispatch_host"],
            conf["jaeger"],
        )
        assert res.status_code == 200


if __name__ == "__main__":
    TestProcessSchedule().test_send("schedule_test_statistic_task@schedule_tests")
    # TestProcessSchedule().test_send("schedule_test_statistic_flow@schedule_tests")
    # TestSubmitSchedule().test_submit("schedule_test_statistic_task@schedule_tests")
