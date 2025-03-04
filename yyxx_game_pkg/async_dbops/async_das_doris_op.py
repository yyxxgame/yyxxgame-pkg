# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2025/02/26
"""
import re
import pandas as pd
from yyxx_game_pkg.async_dbops.base import AsyncDatabaseOperation
from yyxx_game_pkg.dbops.base import DatabaseOperationProxy


class AsyncDasDorisOperation(AsyncDatabaseOperation):
    """
    Async Das doris操作

    接入Tips:
    self.async_op_doris = AsyncDasDorisOperation(doris_conf["db"], das_url, conf_db_name=doris_conf["conf_db"])
    """

    def __init__(self, db_name, das_url, conf_db_name="", *args, **kwargs):
        super().__init__(das_url)
        self.db_name = db_name
        self.das_url = das_url
        self.conf_db_name = conf_db_name

    def replace_sql(self, sql):
        sql = re.sub(r"(\[)(ch_db|db|doris_db|game_db)(])", self.db_name, sql)
        sql = re.sub(r"(\[)(game_conf)(])", self.conf_db_name, sql)
        # TODO临时兼容clickhouse的sql查询(代号X)
        sql = re.sub(r"\b global \b", " ", sql, flags=re.IGNORECASE)
        return sql

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
        sql = self.replace_sql(sql)
        res_df = await self.async_das_client.doris_query(self.das_url, {"sql": sql})
        return res_df

    async def execute(self, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        sql = self.replace_sql(sql)
        b_ok = await self.async_das_client.doris_execute(self.das_url, {"sql": sql})
        return b_ok


class AsyncDasDorisOperationProxy(DatabaseOperationProxy):
    """
    Async Das doris操作代理

    接入Tips:
    DBOperationProxy(AsyncDasDorisOperationProxy)
    """

    __async_op_doris_key__ = "async_op_doris"

    @property
    def _async_op_doris_(self) -> AsyncDasDorisOperation:
        return getattr(self, self.__async_op_doris_key__)

    async def async_get_doris_df(self, sql):
        """
        查询doris库数据

        :param sql: sql语句
        :return: dataframe
        """
        return await self._async_op_doris_.get_all_df(sql)

    async def async_get_doris_one(self, sql):
        """
        查询doris库(单条数据)

        :param sql: sql语句
        :return: series
        """
        return await self._async_op_doris_.get_one_df(sql)

    async def doris_execute(self, sql):
        """
        doris库其他sql操作[insert, update...]

        :param sql: sql语句
        :return: bool
        """
        return await self._async_op_doris_.execute(sql)
