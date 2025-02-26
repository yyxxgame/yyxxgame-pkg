# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2025/02/26
"""
import re
import pandas as pd
from yyxx_game_pkg.dbops.das_api import DasApi
from yyxx_game_pkg.dbops.base import DatabaseOperation, DatabaseOperationProxy


class DorisOperation(DatabaseOperation):
    """
    Doris操作

    接入Tips:
    self.op_doris = DorisOperation(doris_conf["db"], das_url)
    """

    def __init__(self, db_name, das_url, das_api=DasApi, conf_db_name=""):
        super().__init__()
        self.db_name = db_name
        self.das_url = das_url
        self.das_api = das_api
        self.conf_db_name = conf_db_name

    def replace_sql(self, sql):
        sql = re.sub(r"(\[)(ch_db|db|doris_db|game_db)(])", self.db_name, sql)
        sql = re.sub(r"(\[)(game_conf)(])", self.db_name, sql)
        return sql

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
        sql = self.replace_sql(sql)
        res_df = self.das_api.doris_query(self.das_url, {"sql": sql})
        return res_df


class DorisDBOperationProxy(DatabaseOperationProxy):
    """
    Doris操作代理

    接入Tips:
    DBOperationProxy(DorisDBOperationProxy)
    """

    __op_doris_key__ = "op_doris"

    @property
    def _doris_op_(self) -> DorisOperation:
        return getattr(self, self.__op_doris_key__)

    def get_doris_df(self, sql):
        """
        查询doris库数据

        :param sql: sql语句
        :return: dataframe
        """
        return self._doris_op_.get_all_df(sql)

    def get_doris_one(self, sql):
        """
        查询doris库(单条数据)

        :param sql: sql语句
        :return: series
        """
        return self._doris_op_.get_one_df(sql)
