# -*- coding: utf-8 -*-
"""
@File: main.py
@Author: ltw
@Time: 2023/3/23
"""
import logging
import os

import celery.signals
from yyxx_game_pkg.statistic.xcelery.instance import CeleryInstance
from yyxx_game_pkg.statistic.log import logging_init

# 主进程日志配置初始化
logging_init()

os.environ.setdefault("CELERY_CONFIG_MODULE", "config.celery_config")
app = CeleryInstance.get_celery_instance()
logging.info("server main start")


@celery.signals.setup_logging.connect
def setup_logging(*_, **__):
    """
    重写 celery 的日志设置
    :return:
    """
    # worker日志配置初始化
    logging_init()


@celery.signals.worker_process_init.connect
def init_worker(*args, **kwargs):
    # 业务模块初始化
    logging.info("worker_process_init")



# ##################### ##################### ####################
# run:
# celery -A main worker -n your_name -c 1 -Q your_queue
# ##################### ##################### ####################
