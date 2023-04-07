# -*- coding: utf-8 -*-
"""
@File: mysql_op.py
@Author: ltw
@Time: 2023/4/7
"""
from yyxx_game_pkg.dbops.mysql_op import MysqlOperation
from yyxx_game_pkg.helpers import mysql_helper


if __name__ == '__main__':

    # ####### 自定义配置 ######
    config = {
        "host": "10.111.0.10",
        "port": 3306,
        "user": "python",
        "password": "python@h5fumo#//.2022",
        "db": "data_node_api",
        "use_unicode": True
    }
    mysql_helper.get_dbpool(config)
    dbpool = mysql_helper.get_dbpool(config)
    connection = dbpool.get_connection()

    op_mysql = MysqlOperation()

    # insert
    # op_mysql.insert(connection, "api_faq", [[['TCz7NosBP0', 'hGihDm8jaw', 'z3gWfGupGn', '2eZAfrIPtb', '2016-11-23 23:03:48', 'fyaQg7Ejot', 914, '2021-08-18 09:39:18', 'lpkn3KxjK1', '2002-10-28 10:07:06', 'oKeZcW6x0T', 249, 54]]])

    # get_one
    # sql = "select * from api_faq limit 10"
    # print(op_mysql.get_one(sql, connection))

    # get_all
    # sql = "select * from api_faq limit 10"
    # print(op_mysql.get_all(sql, connection))

    # get_one_df
    # 未实现接口 pass

    # get_all_df
    # sql = "select * from api_faq limit 10"
    # print(op_mysql.get_all_df(sql, connection))

    # execute
    sql = "delete from `data_node_api`.`api_faq` where id=3"
    op_mysql.execute(sql, connection)
