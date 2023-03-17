# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

from yyxx_game_pkg.stat.dispatch.dispatch import startup
from yyxx_game_pkg.stat.xcelery.instance import app
from tests.dispatch.rules import rules_auto_import
from yyxx_game_pkg.stat.dispatch.core.manager import RuleManager

if __name__ == "__main__":
    # params
    # --config /your/path/celery_config.py

    # auto load rules
    rules_auto_import()

    # get conf
    conf = app.conf

    # mgr init
    RuleManager().init(conf.get("CUSTOM_TASK_REGISTER_PATH"))

    # http server by fastapi
    startup(conf_jaeger=conf.get("JAEGER"))
