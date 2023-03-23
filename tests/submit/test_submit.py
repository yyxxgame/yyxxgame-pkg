# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/15
import json
import pathlib
import argparse

from yyxx_game_pkg.stat.submit.submit import submit_schedule

if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-c", "--config")
    parser.add_argument("-s", "--schedule")
    args = parser.parse_known_args()[0]

    # schedule
    schedule_name = args.schedule
    if not schedule_name:
        exit()
    # 获取配置
    conf_path = pathlib.Path().joinpath("submit.json")
    if args.config:
        conf_path = args.config

    with open(conf_path, "r") as f:
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
    res_list = submit_schedule(
        schedule_name,
        conf["register_path"],
        conf["dispatch_host"],
        conf["jaeger"],
    )

    for res in res_list:
        print(f"{res.status_code}, {res.content}")
