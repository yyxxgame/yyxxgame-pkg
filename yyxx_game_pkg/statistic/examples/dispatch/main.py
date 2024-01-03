# -*- coding: utf-8 -*-
"""
@File: main.py
@Author: ltw
@Time: 2023/3/22
"""
import os
import argparse
from yyxx_game_pkg.stat.xcelery.instance import CeleryInstance
from public.log import local_log

os.environ.setdefault("CELERY_CONFIG_MODULE", "config.celery_config_test")
app = CeleryInstance.get_celery_instance()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-p", "--port")
    args = parser.parse_known_args()[0]

    port = int(args.port) if args.port else 8080
    local_log("dispatch main start")
    # run
    # python main.py --config /your/path/celery_config.py
    from rules import auto_import
    from stat_pkg.dispatch.dispatch import startup

    # auto load rules
    auto_import()

    # http server by fastapi
    startup(port=port, conf_jaeger=app.conf.get("JAEGER"))

# ##################### ##################### ####################
# run:
# pytho main.py -p 8080
# ##################### ##################### ####################
