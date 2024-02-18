# -*- coding: utf-8 -*-
"""
# @Author   : KaiShin
# @Time     : 2022/2/14
"""
import os
from task_loader import TaskLoader
from yyxx_game_pkg.statistic.xcelery.instance import CeleryInstance
from yyxx_game_pkg.statistic.log import logging_init

logging_init()
os.environ.setdefault("CELERY_CONFIG_MODULE", "config.celery_config")
app = CeleryInstance().get_celery_instance()
app.conf.update(beat_schedule=TaskLoader().load())

# ##################### ##################### ####################
# run:
# scheduler: celery -A main beat --loglevel=info
# worker: celery -A main worker -Q queue_crontab
# ##################### ##################### ####################
