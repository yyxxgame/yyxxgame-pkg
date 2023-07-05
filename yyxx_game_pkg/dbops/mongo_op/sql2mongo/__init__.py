# -*- coding: utf-8 -*-
"""
@File: __init__.py
@Author: ltw
@Time: 2022/8/5
"""
from .sql2mongo import sql_to_spec, create_mongo_spec


def sql_to_mongo_spec(query_sql):
    """
    :param query_sql:
    :return:
    """
    sql_spec = sql_to_spec(query_sql)
    mongo_spec = create_mongo_spec(sql_spec)
    return mongo_spec
