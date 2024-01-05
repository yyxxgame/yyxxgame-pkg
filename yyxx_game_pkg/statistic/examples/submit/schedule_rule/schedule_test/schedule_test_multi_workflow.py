# -*- coding: utf-8 -*-
"""
@File: schedule_test_multi_workflow
@Author: ltw
@Time: 2024/1/3
"""

# 提交任务
# submit.py -c "config/config.test.local.json" -s schedule_test_multi_workflow@schedule_test

# 分发规则名
SCHEDULE_NAME = "schedule_multi_workflow_test"

# 分发队列（选填，队列名@指定优先级，范围0-10，默认为celery@3）
SCHEDULE_QUEUE_NAME = "queue_ltw"

# 分发规则入口名
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "multiple_workflow_instance"

# 计划内容
"""
计划主体
'schedule':[
    {
    'step'： 执行步骤，
    'schedule'：计划任务名（仅支持工作流 必须项)
    }
]
"""
SCHEDULE_CONTENT = [
    {
        "step": 1,
        "schedule": "schedule_test_workflow@schedule_test",
    },
    {
        "step": 2,
        "schedule": "schedule_test_workflow_with_result@schedule_test",
    },
]
