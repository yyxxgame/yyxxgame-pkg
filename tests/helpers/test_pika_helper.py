# -*- coding: utf-8 -*-
"""
@File: test_pika_helper
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.helpers import pika_helper
if __name__ == '__main__':

    # ####### 自定义配置 ######
    config = {
        "host": "10.111.1.16",
        "port": 30372,
        "m_port": 30126,  # 管理端口
        "user": "root",
        "password": "root",
        "v_host": "/",
    }

    pika_conn = pika_helper.get_pika(config)
    print(pika_conn)
