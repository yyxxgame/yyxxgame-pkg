# -*- coding: utf-8 -*-
"""
@File: ch_op.py
@Author: ltw
@Time: 2023/4/4
"""
import pandas as pd
from yyxx_game_pkg.utils.decorator import except_monitor, log_execute_time_monitor
from yyxx_game_pkg.dbops.das_api import DasApi
from yyxx_game_pkg.dbops.base import DatabaseOperation


class CHOperation(DatabaseOperation):
    """
    Clickhouse操作
    """

    def __init__(self, db_name, das_url):
        super().__init__()
        self.db_name = db_name
        self.das_url = das_url

    def get_one_df(self, sql):
        """
        获取单条数据
        :param sql:
        :return:
        """
        res_df = self.get_all_df(sql)
        if not res_df.empty:
            return res_df.iloc[0]
        return pd.Series()

    def get_all_df(self, sql):
        """
        获取所有数据 dataframe
        :param sql:
        :return:
        """
        sql = sql.replace("[ch_db]", self.db_name)
        res_df = DasApi.ch_query(self.das_url, {"sql": sql})
        return res_df

    @except_monitor
    @log_execute_time_monitor()
    def execute(self, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        sql = sql.replace("[ch_db]", self.db_name)
        b_ok = DasApi.ch_execute(self.das_url, {"sql": sql})
        return b_ok
