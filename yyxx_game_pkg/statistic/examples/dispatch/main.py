# -*- coding: utf-8 -*-
"""
@File: main.py
@Author: ltw
@Time: 2023/3/22
"""
import argparse
import logging
import os

from rules.export import auto_import

from yyxx_game_pkg.statistic.dispatch.dispatch import startup
from yyxx_game_pkg.statistic.xcelery.instance import CeleryInstance
from yyxx_game_pkg.statistic.log import logging_init

logging_init()

os.environ.setdefault("CELERY_CONFIG_MODULE", "config.celery_config_test")
app = CeleryInstance.get_celery_instance()
if __name__ == "__main__":
    parser = argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument("-p", "--port")
    args = parser.parse_known_args()[0]

    port = int(args.port) if args.port else 8080
    logging.info("dispatch main start")
    # run
    # python main.py --config /your/path/celery_config.py

    # auto load rules
    auto_import()

    # http server by fastapi
    startup(port=port, conf_jaeger=app.conf.get("JAEGER"))

# ##################### ##################### ####################
# run:
# pytho main.py -p 8080
# ##################### ##################### ####################
