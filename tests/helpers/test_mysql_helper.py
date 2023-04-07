# -*- coding: utf-8 -*-
"""
@File: test_mysql_helper.py
@Author: ltw
@Time: 2023/4/7
"""
from yyxx_game_pkg.helpers import mysql_helper
if __name__ == '__main__':

    # ####### 自定义配置 ######
    config = {
        "host": "10.111.0.10",
        "port": 3306,
        "user": "python",
        "password": "python@sss#//.2022",
        "db": "data_stat",
    }
    mysql_helper.get_dbpool(config)
    dbpool = mysql_helper.get_dbpool(config)
    connection = dbpool.get_connection()
    print(dbpool, connection)
