# -*- coding: utf-8 -*-
"""
@File: mongo_op
@Author: ltw
@Time: 2022/9/20
"""
from abc import abstractmethod

import pandas as pd
from pymongo import MongoClient

from yyxx_game_pkg.dbops.base import DatabaseOperation
from yyxx_game_pkg.dbops.mongo_op.sql2mongo import sql_to_mongo_spec
from yyxx_game_pkg.utils.decorator import (
    except_monitor,
    log_execute_time_monitor,
    singleton_unique,
)


@singleton_unique
class SingletonMongoClient(MongoClient):
    """
    SingletonMongo
    根据db链接确定单例
    """

    def __init__(self, mongo_uri):
        super().__init__(mongo_uri)

    def query_sql(self, sql, collection=None):
        """
        sql 查询接口 仅支持select语法 暂不支持join
        别名仅支持关键字使用[仅能识别 name as player_name 不能识别 name player_name]: as
        支持判断关键字: = > < != in like
        支持聚合关键字: [group by [cols]] sum, count, avg, min, max
        支持排序关键字: order by desc[asc]
        支持翻页关键字: limit 0 [,30]
        :param sql:
        :param collection:
        :return:
        """
        assert collection is not None
        mongo_spec = sql_to_mongo_spec(sql)
        pipeline = []
        for k, val in mongo_spec.items():
            if k == "documents":
                continue
            if not val:
                continue
            pipeline.append({k: val})
        docs = mongo_spec.get("documents")
        cursor = self[collection][docs].aggregate(pipeline)
        return pd.DataFrame(list(cursor))


class PyMongoClient:
    """
    PyMongoClient
    """

    def __init__(self, mongo_uri, db_name):
        self.db_name = db_name
        self.mgo_client = SingletonMongoClient(mongo_uri)

    def __getattr__(self, item):
        return self.mgo_client.__getattr__(item)

    def __getitem__(self, item):
        return self.mgo_client.__getitem__(item)

    @property
    def game_db(self):
        """
        :return:
        """
        return self.mgo_client[self.db_name]

    def query(self, sql):
        """
        :param sql:
        :return:
        """
        return self.mgo_client.query_sql(sql, self.db_name)


class MongoOperation(DatabaseOperation):
    """
    MongoOperation
    """

    @abstractmethod
    def get_mongo_info(self, *args, **kwargs) -> {str, str}:
        """
        :param args:
        :param kwargs:
        :return:
        """

    @staticmethod
    def new_client(mongo_url, game_db) -> PyMongoClient:
        """
        :param mongo_url:
        :param game_db:
        :return:
        """
        mgo_client = PyMongoClient(mongo_url, game_db)
        return mgo_client

    @except_monitor
    @log_execute_time_monitor()
    def get_one_df(self, sql, *args, **kwargs):
        """
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        mongo_url, game_db = self.get_mongo_info(*args, **kwargs)
        res_df = self.new_client(mongo_url, game_db).query(sql)
        return res_df.iloc[0] if not res_df.empty else res_df

    @except_monitor
    @log_execute_time_monitor()
    def get_all_df(self, sql, *args, **kwargs):
        """
        :param sql:
        :param args:
        :param kwargs:
        :return:
        """
        mongo_url, game_db = self.get_mongo_info(*args, **kwargs)
        res_df = self.new_client(mongo_url, game_db).query(sql)
        return res_df
