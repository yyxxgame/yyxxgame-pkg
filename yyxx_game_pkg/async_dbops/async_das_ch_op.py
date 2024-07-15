# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2023/11/8
"""

import pandas as pd

from .base import AsyncDatabaseOperation


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
