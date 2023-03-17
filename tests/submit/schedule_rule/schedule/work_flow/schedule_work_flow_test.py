# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/17


# 工作流规则名(标识用)
SCHEDULE_NAME = "schedule_work_flow_test"

# 分发队列（选填，队列名@指定优先级，范围0-10，默认为celery@3）
SCHEDULE_QUEUE_NAME = "queue_test"
# SCHEDULE_QUEUE_NAME = 'queue_kudu*@9'

# 工作流入口名（！！！必填，勿更改！！！）
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "work_flow_instance"

# 计划内容
SCHEDULE_CONTENT = [
    {
        "step": 1,
        "schedule": "schedule_statistic_task_test",
    },
    {
        "step": 1,
        "schedule": "schedule_statistic_task_test",
        "custom_content": {"kwargs_list": [{"x": 100, "y": 200}]},
    },
    {
        "step": 1,
        "schedule": "schedule_statistic_task_test",
        "custom_content": {"kwargs_list": [{"x": 1000, "y": 2000}]},
    },
    {
        "step": 2,
        "schedule": "schedule_statistic_collect_test",
    },
    {
        "step": 2,
        "schedule": "schedule_statistic_collect_test",
    },
    {
        "step": 3,
        "schedule": "schedule_statistic_collect_test",
    },
    # {
    #     "step": 4,
    #     "schedule": "schedule_statistic_collect_test",
    # },
]
