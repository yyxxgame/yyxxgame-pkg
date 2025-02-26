# -*- coding: utf-8 -*-
"""
@File: ch_op.py
@Author: ltw
@Time: 2023/4/4
"""
import pandas as pd
from yyxx_game_pkg.utils.decorator import except_monitor, log_execute_time_monitor
from yyxx_game_pkg.dbops.das_api import DasApi
from yyxx_game_pkg.dbops.base import DatabaseOperation, DatabaseOperationProxy


class CHOperation(DatabaseOperation):
    """
    Clickhouse操作
    """

    def __init__(self, db_name, das_url, das_api=DasApi):
        super().__init__()
        self.db_name = db_name
        self.das_url = das_url
        self.das_api = das_api

    def get_one_df(self, sql):
        """
        获取单条数据
        :param sql:
        :return:
        """
        res_df = self.get_all_df(sql)
        if not res_df.empty:
            return res_df.iloc[0]
        return pd.Series(dtype=str)

    def get_all_df(self, sql):
        """
        获取所有数据 dataframe
        :param sql:
        :return:
        """
        sql = sql.replace("[ch_db]", self.db_name)
        res_df = self.das_api.ch_query(self.das_url, {"sql": sql})
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
        b_ok = self.das_api.ch_execute(self.das_url, {"sql": sql})
        return b_ok


class CHOperationProxy(DatabaseOperationProxy):
    """
    Clickhouse操作代理

    接入Tips:
    DBOperationProxy(CHOperationProxy)
    """

    __op_ch_key__ = "op_ch"

    @property
    def _ch_op_(self) -> CHOperation:
        return getattr(self, self.__op_ch_key__)

    def get_ch_df(self, sql):
        """
        查询clickhouse库数据

        :param sql: sql语句
        :return: dataframe
        """
        return self._ch_op_.get_all_df(sql)

    def get_split_ch_df(self, sql, split_lst, size=5000):
        """
        查询ch库 多条sql, 查询字段需保持一致
        自行处理聚合操作

        :param sql: sql语句列表
        :param split_lst: 需切分的参数
        :param size: 切分长度
        :return: dataframe
        """
        if not split_lst:
            return self.get_ch_df(sql)
        split_lst = list(map(int, split_lst))
        sql_lst = self.split_sql(sql, split_lst, size)
        res_df_lst = []
        for _sql in sql_lst:
            res_df = self.get_ch_df(_sql)
            res_df_lst.append(res_df)
        return pd.concat(res_df_lst, ignore_index=True)

    def get_ch_one(self, sql):
        """
        查询clickhouse库(单条数据)

        :param sql: sql语句
        :return: series
        """
        return self._ch_op_.get_one_df(sql)

    def ch_execute(self, sql):
        """
        clickhouse库其他sql操作[insert, update...]

        :param sql: sql语句
        :return: bool
        """
        return self._ch_op_.execute(sql)
