# -*- coding: utf-8 -*-
"""
@File: test_redis_helper
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.utils import redis_helper
if __name__ == '__main__':

    # ####### 自定义配置 ######
    class CustomConfig(redis_helper.RedisConfig):
        HOST = "10.111.1.16"
        PORT = 30016
        DB = 6
        PASSWORD = "fumo!python"


    redis_handle = redis_helper.RedisHelper(CustomConfig)
    print(redis_handle)
    # redis_handle.hget(xxx)
    # ...
