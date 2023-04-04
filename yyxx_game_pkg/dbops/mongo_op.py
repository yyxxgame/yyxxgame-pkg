# -*- coding: utf-8 -*-
"""
@File: mongo_op
@Author: ltw
@Time: 2022/9/20
"""
import pandas as pd
from yyxx_game_pkg.utils.decorator import except_monitor, log_execute_time_monitor
from yyxx_game_pkg.dbops.das_api import DasApi
from yyxx_game_pkg.dbops.base import DatabaseOperation


class MongoOperation(DatabaseOperation):
    def __init__(self, das_url):
        super().__init__()
        self.das_url = das_url

    @except_monitor
    @log_execute_time_monitor()
    def get_one_df(self, sql, mongo_url):
        res_df = DasApi.mongo_query(self.das_url, {"sql": sql, "server": mongo_url})
        if res_df is None:
            return pd.DataFrame()
        return res_df if res_df.empty else res_df.iloc[0]

    @except_monitor
    @log_execute_time_monitor()
    def get_all_df(self, sql, mongo_url):
        res_df = DasApi.mongo_query(self.das_url, {"sql": sql, "server": mongo_url})
        if res_df is None:
            return pd.DataFrame()
        return res_df
