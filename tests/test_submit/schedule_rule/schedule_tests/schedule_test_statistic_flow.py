# -*- coding: utf-8 -*-
"""
@File: schedule_test_workflow
@Author: ltw
@Time: 2024/1/3
"""
# 规则名 [仅做标识用, 无其他含义 2024.01.03]
SCHEDULE_NAME = "schedule_test_statistic_flow"

# 分发队列（选填，队列名@指定优先级，范围0-10，默认为celery@3）
SCHEDULE_QUEUE_NAME = "queue_test"

# 分发规则入口名
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "statistic_flow_instance"

# 计划内容
SCHEDULE_CONTENT = [
    {
        "step": '1',
        "schedule": "tests_task_1",  # 规则名 [仅做标识用, 无其他含义 2024.01.03]
        # 解析工作流子任务规则入口名 [必需 2023.01.03新增]

        # 根据旧schedule规则新增配置行
        # work_template_pull_base => 'rule_instance' = 'pull_task_instance'
        # work_template_pull_collect => 'rule_instance' = 'pull_collect_instance'
        # work_template_task_base => 'rule_instance' = 'statistic_task_instance'
        # work_template_task_collect => 'rule_instance' = 'statistic_collect_instance'

        "rule_instance": "statistic_task_instance",
        "custom_content": {
            "statistic_ids": [1],
            "server_id_slice_size": 1,
            "date_interval": "ACROSS_DAY",
            "appoint_server_ids": [999989, 999999, 999888, 999887],
            "ex_params": {"op_type": 1},
        },
    },
    {
        # 跨服合服信息统计
        "step": '2',
        "schedule": "tests_task_2",
        "rule_instance": "statistic_task_instance",
        "custom_content": {
            "statistic_ids": [2],
            "server_id_slice_size": 1,
            "date_interval": "ACROSS_DAY",
            "appoint_server_ids": [999989, 999999, 999888],
            "ex_params": {"is_cross": 1},
        },
    },
    {
        "step": 3,
        "schedule": "tests_task_3",
        "rule_instance": "statistic_collect_instance",
        "custom_content": {
            "statistic_ids": [3],
            "server_id_slice_size": 1,
            "date_interval": "ACROSS_DAY",
            "appoint_server_ids": [999989, 999999, 999888],
        },
    },
]
