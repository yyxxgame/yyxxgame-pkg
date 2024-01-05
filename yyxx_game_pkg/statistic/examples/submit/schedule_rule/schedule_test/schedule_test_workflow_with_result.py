# -*- coding: utf-8 -*-
"""
@File: schedule_test_workflow_with_result
@Author: ltw
@Time: 2024/1/3
"""

# 提交任务
# submit.py -c "config/config.test.local.json" -s schedule_test_workflow_with_result@schedule_test

# 规则名 [仅做标识用, 无其他含义 2024.01.03]
SCHEDULE_NAME = "schedule_test_work_flow_with_result"

# 分发队列（选填，队列名@指定优先级，范围0-10，默认为@3）
SCHEDULE_QUEUE_NAME = "queue_ltw"

# 分发规则入口名
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "work_flow_instance"

# 计划内容
SCHEDULE_CONTENT = [
    {
        "step": 1,
        "schedule": "test_task_1_w",  # 规则名 [仅做标识用, 无其他含义 2024.01.03]
        # 解析工作流子任务规则入口名 [必需 2023.01.03新增]
        "rule_instance": "statistic_task_instance",
        "custom_content": {
            "statistic_ids": [1],
            "server_id_slice_size": 50,
            "date_interval": "ACROSS_DAY",
            "ex_params": {"op_type": 1},
        },
    },
    {
        "step": 2,
        "schedule": "test_task_2_w",
        "rule_instance": "statistic_collect_instance",
        "custom_content": {
            "statistic_ids": [2],
            "server_id_slice_size": 20,
            "date_interval": "ACROSS_DAY",
            "appoint_server_ids_by_sql": """
                SELECT DISTINCT id
                FROM svr_server
                WHERE id in(999989, 999999)
            """,
            "ex_params": {"is_cross": 1},
        },
    },
    {
        "step": 3,
        "schedule": "test_task_3_w",
        "rule_instance": "statistic_collect_instance",
        "custom_content": {
            "statistic_ids": [3],
            "server_id_slice_size": -1,
            "date_interval": "ACROSS_DAY",
        },
    },
]
