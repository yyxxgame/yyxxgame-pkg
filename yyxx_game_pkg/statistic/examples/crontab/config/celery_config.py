# -*- coding: utf-8 -*-
"""
celery 配置环境
"""

# ############################# 自定义配置 start #############################
# 任务注册路径(切勿随意修改)
CUSTOM_TASK_REGISTER_PATH = "task_register"

# 定时任务队列
CRONTAB_QUEUE = "queue_crontab_ltw"

# rabbitmq配置
RMQ_CONFIG = {
    "host": "10.111.1.6",
    "port": 30372,
    "m_port": 30126,  # 管理端口
    "user": "root",
    "password": "root",
    "v_host": "/",
}

# redis配置
REDIS_CONFIG = {
    "host": "10.111.1.6",
    "port": 30016,
    "db": 6,
    "password": "fumo!python",
    "overdue_seconds": 60 * 60 * 24,
}

# 发行标识符
PUBLISH_FLAG = "fumo_test"

# jaeger上报配置
JAEGER = {
    # "service_name": "[master](test)crontab",
    # "jaeger_host": "10.0.3.124",
    # "jaeger_port": 6831,
}
# ############################# 自定义配置 end #############################

# ############################# celery系统配置 start #############################
# broker
broker_url = f"amqp://root:root@{RMQ_CONFIG['host']}:{RMQ_CONFIG['port']}/"

# backend
result_backend = f"redis://:{REDIS_CONFIG['password']}@{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/1"

# 时区
timezone = "Asia/Shanghai"

# 优先级队列设置
task_acks_late = True
worker_prefetch_multiplier = 1

# include
include = [CUSTOM_TASK_REGISTER_PATH]

# 非常重要,有些情况下可以防止死锁
# CELERYD_FORCE_EXECV = True

# 每个worker执行了多少任务就会死掉
worker_max_tasks_per_child = 200

# 任务结果过期时间（秒）
result_expires = 60 * 60 * 1 + 60

# 不移除 root logger 的 handler
worker_hijack_root_logger = False
# ############################# celery系统配置 end #############################
