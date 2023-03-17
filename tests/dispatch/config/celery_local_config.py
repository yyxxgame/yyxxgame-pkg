# -*- coding: utf-8 -*-

"""
celery 配置环境
"""

# region
"""
自定义配置
"""
# 任务注册路径(切勿随意修改)
CUSTOM_TASK_REGISTER_PATH = "tests.xcelery.task_register"


# rabbitmq配置
RMQ_CONFIG = {
    "host": "192.168.113.61",
    "port": 5672,
    "m_port": 15672,  # 管理端口
    "user": "root",
    "password": "root",
    "v_host": "/",
}

# redis配置
REDIS_CONFIG = {
    "host": "192.168.113.61",
    "port": 16379,
    "db": 6,
    "password": "openIM",
    "overdue_seconds": 60 * 60 * 24,
}

# 发行标识符
PUBLISH_FLAG = "my_test"

# jaeger
JAEGER = {
    "service_name": "dispatch",
    "jaeger_host": "192.168.113.61",
    # "jaeger_host": "localhost",
    "jaeger_port": 6831,
}
# endregion

"""
系统配置
"""
# broker
broker_url = "amqp://root:root@{}:{}/".format(RMQ_CONFIG["host"], RMQ_CONFIG["port"])

# backend
result_backend = "redis://:{}@{}:{}/1".format(
    REDIS_CONFIG["password"], REDIS_CONFIG["host"], REDIS_CONFIG["port"]
)

# 时区
timezone = "Asia/Shanghai"

# include
include = [CUSTOM_TASK_REGISTER_PATH]


# 每个worker执行了多少任务就会死掉
worker_max_tasks_per_child = 200

# 任务结果过期时间（秒）
result_expires = 60 * 60 * 1 + 1800
