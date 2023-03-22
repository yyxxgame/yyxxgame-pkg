# -*- coding: utf-8 -*-
"""
@File: test_pika_helper
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.utils import pika_helper
if __name__ == '__main__':

    # ####### 自定义配置 ######
    class CustomConfig(pika_helper.PikaConfig):
        USER = "root"
        PASSWORD = "root"
        HOST = "10.111.1.16"
        PORT = 30372
        M_PORT = 30126

    pika_conn = pika_helper.connection(CustomConfig)
    print(pika_conn)
