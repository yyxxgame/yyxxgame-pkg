# -*- coding: utf-8 -*-
"""
@File: test_redis_helper
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.helpers import redis_helper
if __name__ == '__main__':

    # ####### 自定义配置 ######
    config = {
        "host": "10.111.1.16",
        "port": 30016,
        "db": 6,
        "password": "fumo!python",
        "overdue_seconds": 60 * 60 * 24,
    }

    redis_handle = redis_helper.get_redis(config)
    print(redis_handle)
    # redis_handle.hget(xxx)
    # ...
