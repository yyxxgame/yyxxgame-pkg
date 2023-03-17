# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/15
import json

from yyxx_game_pkg.stat.submit.submit import submit_schedule

if __name__ == "__main__":
    import os

    # 获取配置
    conf_json = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submit.json")

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
    with open(conf_json, "r") as f:
        conf = json.load(f)

    # 参数配置获取
    import sys

    if len(sys.argv) > 1:
        conf["schedule_name"] = sys.argv[1]

    res_list = submit_schedule(
        conf["schedule_name"],
        conf["register_path"],
        conf["dispatch_host"],
        conf["jaeger"],
    )

    for res in res_list:
        print(f"{res.status_code}, {res.content}")
