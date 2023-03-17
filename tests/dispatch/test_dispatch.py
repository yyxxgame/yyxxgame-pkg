# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

from yyxx_game_pkg.stat.dispatch.dispatch import startup
from yyxx_game_pkg.stat.xcelery.instance import CeleryInstance
from tests.dispatch.rules import rules_auto_import
from yyxx_game_pkg.stat.dispatch.core.manager import RuleManager

if __name__ == "__main__":
    # params
    # --config /path/celery_config.py

    # auto load rules
    rules_auto_import()

    # get conf
    conf = CeleryInstance._get_config()

    # mgr init
    RuleManager().init(conf.CUSTOM_TASK_REGISTER_PATH)

    # http server by fastapi
    startup(conf_jaeger=conf.JAEGER)
