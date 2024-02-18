# -*- coding: utf-8 -*-
"""
@File: schedule_test_single_statistic.py
@Author: ltw
@Time: 2023/3/24
"""

# 提交任务
# submit.py -c "config/config.test.local.json" -s schedule_test_single_statistic@schedule_test

# 规则名 [仅做标识用, 无其他含义 2024.01.03]
SCHEDULE_NAME = "schedule_test_single_statistic_1"

# 消费队列名 [必需]
SCHEDULE_QUEUE_NAME = "queue_ltw@3"

# 分发规则入口名 [必需]
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "statistic_task_instance"

# 计划内容
SCHEDULE_CONTENT = [
    {
        "server_id_slice_size": 2,
        # "appoint_server_ids": [1],
        "appoint_server_ids_by_sql": """
            SELECT DISTINCT id
            FROM svr_server
            WHERE id in(999989, 999999)
        """,
        "statistic_ids": [2],
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
