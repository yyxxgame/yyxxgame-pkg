# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/16
import os
from yyxx_game_pkg.stat.xcelery.instance import CeleryInstance

os.environ.setdefault("CELERY_CONFIG_MODULE", "config.celery_local_config")
app = CeleryInstance.get_celery_instance()
if __name__ == "__main__":
    pass
