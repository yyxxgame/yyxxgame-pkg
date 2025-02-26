# -*- coding: utf-8 -*-
"""
@File: async_es_op.py
@Author: ltw
@Time: 2023/6/14
"""
import pandas as pd
from .base import AsyncDatabaseOperation
from yyxx_game_pkg.dbops.base import DatabaseOperationProxy


class AsyncDasESOperation(AsyncDatabaseOperation):
    """
    Async Das ElasticSearch 操作
    """

    def __init__(self, broker, topic, suffix, das_url):
        super().__init__(das_url)
        self.suffix = suffix
        self.broker = broker
        self.topic = topic

    async def insert(self, data_rows, kafka_addr=None, topic=None):
        """
        :param kafka_addr:
        :param topic:
        :param data_rows:
        :return:
        """
        kafka_addr = kafka_addr if kafka_addr else self.broker
        topic = topic if topic else self.topic
        post_data = {"kafka_addr": kafka_addr, "topic": topic, "data_rows": data_rows}
        res = await self.async_das_client.es_insert(self.das_url, post_data)
        return res

    async def get_all_df(self, sql, search_from=-1, fetch_size=50000):
        """
        :param sql:
        :param search_from:
        :param fetch_size:
        :return:
        """
        # "select * from log_play[_suffix] where xxx"
        if search_from >= 10000:
            # api会报错 直接返回空
            # es分页查询只能查10000条, 若下载只能一次性查询所需下载数目[最多50w条(fetch_size参数)]
            # 已和运营约定暂时上限10w条 ltw
            return pd.DataFrame()
        sql = sql.replace("[_suffix]", self.suffix)
        res_df = await self.async_das_client.es_query(
            self.das_url,
            {
                "sql": sql,
                "engine": 1,
                "search_from": search_from,
                "fetch_size": fetch_size,
            },
        )
        return res_df


class AsyncDasESOperationProxy(DatabaseOperationProxy):
    """
    ElasticSearch操作代理

    接入Tips:
    DBOperationProxy(AsyncDasESOperationProxy)
    """

    __async_op_es_key__ = "async_op_es"

    @property
    def _async_op_es_(self) -> AsyncDasESOperation:
        return getattr(self, self.__async_op_es_key__)

    async def async_get_es_df(self, sql, search_from=-1, fetch_size=50000):
        """
        查询elasticsearch库数据

        :param sql: sql语句
        :param search_from:
        :param fetch_size:
        :return: dataframe
        """
        sql = sql.replace(" server_id between", " server_id::INT between")
        sql = sql.replace("(server_id between", "(server_id::INT between")
        return await self._async_op_es_.get_all_df(sql, search_from, fetch_size)
