# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14
import os
from yyxx_game_pkg.stat.dispatch.dispatch import startup
from yyxx_game_pkg.stat.xcelery.instance import CeleryInstance
from tests.dispatch.rules import rules_auto_import

os.environ.setdefault('CELERY_CONFIG_MODULE', 'config.celery_local_config')
app = CeleryInstance.get_celery_instance()

if __name__ == "__main__":
    # params
    # --config /your/path/celery_config.py

    # auto load rules
    rules_auto_import()

    # http server by fastapi
    startup(conf_jaeger=app.conf.get("JAEGER"))
