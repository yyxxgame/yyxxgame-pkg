# -*- coding: utf-8 -*-
"""
@File: submit.py
@Author: ltw
@Time: 2023/3/22
"""
import argparse
import datetime
import json
import logging
import pathlib
import sys

from yyxx_game_pkg.statistic.log import logging_init
from yyxx_game_pkg.statistic.submit.export import submit_schedule

logging_init()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-c", "--config")
    parser.add_argument("-s", "--schedule")
    args = parser.parse_known_args()[0]

    # schedule
    schedule_name = args.schedule
    if not schedule_name:
        sys.exit()
    # 获取配置
    conf_path = pathlib.Path(__file__).parent.absolute().joinpath("config/config.json")
    if args.config:
        conf_path = args.config

    with open(conf_path, "r", encoding="utf8") as f:
        conf = json.load(f)
    # conf = {
    #     "schedule_name": "schedule_work_flow_test",
    #     "register_path": "tests.submit.schedule_rule.statistic_task",
    #     "dispatch_host": "http://localhost:8080",
    #     "jaeger": {
    #         "service_name": "submit",
    #         "jaeger_host": "192.168.113.61",
    #         "jaeger_port": 6831,
    #     },
    # }
    res = submit_schedule(
        schedule_name,
        conf["register_path"],
        conf["dispatch_host"],
        conf["jaeger"],
    )

    logging.info("[%s]: status: %s, content: %s", datetime.datetime.now(), res.status_code, res.content)

# ##################### ##################### ####################
# run:
# -c 指定配置文件[可选]
# -s 指定任务schedule[必填]
# 默认路径 schedule_rule/schedule/*.py
# 提交示例: python submit.py -c "config/config.json" -s schedule_test_single_statistic

# 自定义路径(schedule_rule 目录下) schedule_rule/schedule_test/*.py
# 提交示例: python submit.py -s schedule_test_workflow@schedule_test
# ##################### ##################### ####################
