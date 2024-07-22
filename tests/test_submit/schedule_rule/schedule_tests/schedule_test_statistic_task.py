# -*- coding: utf-8 -*-
"""
@File: schedule_test_single_statistic.py
@Author: ltw
@Time: 2023/3/24
"""

# 规则名 [仅做标识用, 无其他含义 2024.01.03]
SCHEDULE_NAME = "schedule_test_statistic_task"

# 消费队列名 [必需]
SCHEDULE_QUEUE_NAME = "queue_test@3"

# 分发规则入口名 [必需]
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "statistic_task_instance"

# 计划内容
SCHEDULE_CONTENT = [
    {
        "server_id_slice_size": 2,
        "appoint_server_ids": [999989, 999999],
        "statistic_ids": [1],
        # ********* test region done *******
        "date_appoint": ["2022-05-12 00:00:00", "2022-05-30 23:59:59"],
        # ********* test region done *******
        # "date_interval": "ACROSS_DAY",

        # ********* test region done *******
        # "date_appoint": ["2022-05-12 00:00:00", "2022-05-30 23:59:59"],
        # "date_interval": "SPLIT_DATE_BY_DAY",
        # ********* test region done *******
        "ex_params": {},
    }
]
