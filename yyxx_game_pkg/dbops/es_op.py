# -*- coding: utf-8 -*-
"""
@File: es_op.py
@Author: ltw
@Time: 2023/4/4
"""
import pandas as pd
from yyxx_game_pkg.dbops.das_api import DasApi
from yyxx_game_pkg.dbops.base import DatabaseOperation
from yyxx_game_pkg.logger.log import root_log as local_log


class ESOperation(DatabaseOperation):
    """
    ElasticSearch 操作
    """

    def __init__(self, broker, topic, suffix, das_url):
        super().__init__()
        self.suffix = suffix
        self.das_url = das_url
        self.broker = broker
        self.topic = topic

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
        res = DasApi.es_insert(self.das_url, post_data)
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
            local_log("search by page limit 10000 entries, now from=10000")
            return pd.DataFrame()
        sql = sql.replace("[_suffix]", self.suffix)
        res_df = DasApi.es_query(
            self.das_url,
            {
                "sql": sql,
                "engine": 1,
                "search_from": search_from,
                "fetch_size": fetch_size,
            },
        )
        return res_df
