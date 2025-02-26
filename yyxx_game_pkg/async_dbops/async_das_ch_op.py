# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2023/11/8
"""

import pandas as pd

from .base import AsyncDatabaseOperation
from yyxx_game_pkg.dbops.base import DatabaseOperationProxy


class AsyncDasCHOperation(AsyncDatabaseOperation):
    """
    Async Das Clickhouse操作
    """

    def __init__(self, db_name, das_url):
        super().__init__(das_url)
        self.db_name = db_name
        self.das_url = das_url

    async def get_one_df(self, sql):
        """
        获取单条数据
        :param sql:
        :return:
        """
        res_df = await self.get_all_df(sql)
        if not res_df.empty:
            return res_df.iloc[0]
        return pd.Series(dtype=str)

    async def get_all_df(self, sql) -> pd.DataFrame:
        """
        获取所有数据 dataframe
        :param sql:
        :return:
        """
        sql = sql.replace("[ch_db]", self.db_name)
        res_df = await self.async_das_client.ch_query(self.das_url, {"sql": sql})
        return res_df

    async def execute(self, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        sql = sql.replace("[ch_db]", self.db_name)
        b_ok = await self.async_das_client.ch_execute(self.das_url, {"sql": sql})
        return b_ok


class AsyncDasCHOperationProxy(DatabaseOperationProxy):
    """
    Async Das Clickhouse操作代理

    接入Tips:
    DBOperationProxy(AsyncDasCHOperationProxy)
    """

    __async_op_ch_key__ = "async_op_ch"

    @property
    def _async_op_ch_(self) -> AsyncDasCHOperation:
        return getattr(self, self.__async_op_ch_key__)

    async def async_get_ch_df(self, sql):
        """
        查询clickhouse库数据

        :param sql: sql语句
        :return: dataframe
        """
        return await self._async_op_ch_.get_all_df(sql)

    async def async_get_ch_one(self, sql):
        """
        查询clickhouse库(单条数据)

        :param sql: sql语句
        :return: series
        """
        return await self._async_op_ch_.get_one_df(sql)
