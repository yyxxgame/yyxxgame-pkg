# -*- coding: utf-8 -*-
"""
celery 配置环境
"""

# ############################# 自定义配置 start #############################
# 任务注册路径(切勿随意修改)
CUSTOM_TASK_REGISTER_PATH = "task_register"

# redis配置
REDIS_CONFIG = {
    "host": "127.0.0.1",
    "port": 19376,
    "db": 3,
    "password": "",
    "overdue_seconds": 60 * 60 * 24,
}

# jaeger上报配置
JAEGER = {}
# ############################# 自定义配置 end #############################

# ############################# celery系统配置 start #############################
REDIS_URL = (
    f"redis://:{REDIS_CONFIG['password']}@{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}"
)

# broker
broker_url = f"{REDIS_URL}/3"

# backend
result_backend = f"{REDIS_URL}/1"


# include
include = [CUSTOM_TASK_REGISTER_PATH]

# 非常重要,有些情况下可以防止死锁
# CELERYD_FORCE_EXECV = True

# 时区
timezone = "Asia/Shanghai"

# 优先级队列设置
task_acks_late = True
worker_prefetch_multiplier = 1

# 每个worker执行了多少任务就会死掉
worker_max_tasks_per_child = 200

# 任务结果过期时间（秒）
result_expires = 60 * 60 * 1 + 60

# 不移除 root logger 的 handler
worker_hijack_root_logger = False

# task_compression = "gzip"
# result_compression = "gzip"
# ############################# celery系统配置 end #############################
