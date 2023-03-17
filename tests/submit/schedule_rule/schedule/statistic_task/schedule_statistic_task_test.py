# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/15

# -*- coding: utf-8 -*-

# 分发规则名
SCHEDULE_NAME = "schedule_test"

# 分发队列（选填，队列名@指定优先级，范围0-10，默认为celery@3）
SCHEDULE_QUEUE_NAME = "queue_test"

# 分发规则入口名
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "add"

# 计划内容
SCHEDULE_CONTENT = [{"kwargs_list": [{"x": 1, "y": 2}]}]
