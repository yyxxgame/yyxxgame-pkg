# -*- coding: utf-8 -*-

# 分发规则名
SCHEDULE_NAME = "collect_test"

# 分发队列（选填，队列名@指定优先级，范围0-10，默认为celery@3）
SCHEDULE_QUEUE_NAME = "queue_test"

# 分发规则入口名
SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = "gather"

"""
该类型统计，获取multi类型统计返回的数据，进行2次处理
"""
# 计划内容
SCHEDULE_CONTENT = [{"kwargs_list": [{"gather": "hello"}]}]
