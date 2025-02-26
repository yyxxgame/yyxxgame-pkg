# -*- coding: utf-8 -*-
"""
@File: es_op.py
@Author: ltw
@Time: 2023/4/4
"""
import logging
import traceback
import pandas as pd
from yyxx_game_pkg.dbops.das_api import DasApi
from yyxx_game_pkg.dbops.base import DatabaseOperation, DatabaseOperationProxy
from yyxx_game_pkg.utils import xListStr
from yyxx_game_pkg.statistic.log import local_log


class ESOperation(DatabaseOperation):
    """
    ElasticSearch 操作
    """

    def __init__(self, broker, topic, suffix, das_url, das_api=DasApi):
        super().__init__()
        self.suffix = suffix
        self.das_url = das_url
        self.broker = broker
        self.topic = topic
        self.das_api = das_api

    def insert(self, data_rows, kafka_addr=None, topic=None):
        """
        :param kafka_addr:
        :param topic:
        :param data_rows:
        :return:
        """
        kafka_addr = kafka_addr if kafka_addr else self.broker
        topic = topic if topic else self.topic
        post_data = {"kafka_addr": kafka_addr, "topic": topic, "data_rows": data_rows}
        res = self.das_api.es_insert(self.das_url, post_data)
        return res

    def get_all_df(self, sql, search_from=-1, fetch_size=50000):
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
            logging.info("search by page limit 10000 entries, now from=%s", search_from)
            return pd.DataFrame()
        sql = sql.replace("[_suffix]", self.suffix)
        res_df = self.das_api.es_query(
            self.das_url,
            {
                "sql": sql,
                "engine": 1,
                "search_from": search_from,
                "fetch_size": fetch_size,
            },
        )
        return res_df


class ESOperationProxy(DatabaseOperationProxy):
    """
    ElasticSearch操作代理

    接入Tips:
    DBOperationProxy(ESOperationProxy)
    """

    __op_es_key__ = "op_es"

    @property
    def _op_es_(self) -> ESOperation:
        return getattr(self, self.__op_es_key__)

    def get_es_df(self, sql, search_from=-1, fetch_size=50000):
        """
        查询elasticsearch库数据

        :param sql: sql语句
        :param search_from:
        :param fetch_size:
        :return: dataframe
        """
        sql = sql.replace(" server_id between", " server_id::INT between")
        sql = sql.replace("(server_id between", "(server_id::INT between")
        return self._op_es_.get_all_df(sql, search_from, fetch_size)

    def get_es_table_columns(self, table_name, only_column=True, reg=""):
        columns_df = self._op_es_.get_all_df(sql=f"DESC {table_name}")
        if reg:
            columns_df = columns_df[columns_df["column"].str.contains(reg)]
        if only_column:
            return columns_df["column"].tolist()
        return columns_df

    def insert_result_es_stat(self, res_df, event, stat_type=""):
        """
        插入数据到elasticsearch库(统计)

        :param res_df: insert 数据 (dataframe 格式)
        :param event: 匹配es索引
            stat_player_slice_* -> stat_common_player
            stat_log_pull_* -> stat_log_pull
            其他 -> stat_common
        :param stat_type: 筛选关键字 (select * from stat_common where stat_type = {stat_type})
        :return:
        """
        fields = res_df.columns.tolist()
        results = [res_df.values.tolist()]
        size_results = xListStr.split_list(results, split_size=500)
        try:
            for res in size_results:
                res_df = pd.DataFrame(res, columns=fields)
                res_df["event"] = event
                res_df["stat_type"] = stat_type
                data_rows = res_df.to_dict("records")
                self._op_es_.insert(data_rows)
        except Exception as e:
            exc = traceback.format_exc()
            local_log(f"insert_result_es_stat {e} {exc}")

    def insert_result_es_pull(self, fields, results, pull_type):
        """
        插入数据到elasticsearch库(捞数据)

        :param fields: 字段名 [column, ...]
        :param results: 数据集 [[data..]]
        :param pull_type: 筛选关键字 select * from stat_log_pull where pull_type = {pull_type}
        :return:
        """
        size_results = xListStr.split_list(results, split_size=500)
        for res in size_results:
            res_df = pd.DataFrame(res, columns=fields)
            res_df["pull_type"] = pull_type
            res_df["event"] = "stat_log_pull"
            data_rows = res_df.to_dict("records")
            self._op_es_.insert(data_rows)

    def insert_pull_result_df_to_es(self, res_df, pull_type):
        """
        插入数据到elasticsearch库(捞数据)

        :param res_df: 插入数据(dataframe)
        :param pull_type: 筛选关键字 select * from stat_log_pull where pull_type = {pull_type}
        :return:
        """
        self.insert_result_es_pull(res_df.columns.tolist(), [res_df.values.tolist()], pull_type)
