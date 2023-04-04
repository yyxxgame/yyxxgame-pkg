# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2022/8/1
"""
das_api python 调用
"""
import re
import requests
import numpy as np
import pandas as pd
import ujson as json


def trans_unsupported_types(val):
    """
    转化json.dumps不支持的数据类型 : int64, bytes, ...
    :param val:
    :return:
    """
    if isinstance(val, dict):
        new_dict = {}
        for k, _v in val.items():
            k = trans_unsupported_types(k)
            _v = trans_unsupported_types(_v)
            new_dict[k] = _v
        return new_dict
    if isinstance(val, list):
        for idx, _v in enumerate(val):
            _v = trans_unsupported_types(_v)
            val[idx] = _v
    elif isinstance(val, np.int64):
        val = int(val)
    elif isinstance(val, bytes):
        val = val.decode(encoding="utf8")
    return val


class DasApi:
    """
    DasApi py
    """

    @staticmethod
    def _post(das_url, post_type, post_data):
        url = f"{das_url}/{post_type}"
        post_data = trans_unsupported_types(post_data)
        res = requests.post(json=post_data, url=url, timeout=600)
        return res.ok, res.content

    @staticmethod
    def mongo_query(das_url, post_data):
        """
        sql语句 查询 mongo 库
        :param das_url: das_http_url
        :param post_data: {
            'sql': sql,             # sql语句 支持sql 和 js_sql
            'server': mongo_url     # mongo链接
        }
        :return:
        """
        b_ok, res = DasApi._post(das_url, "das/mgo/query", post_data=post_data)
        if not b_ok:
            raise Exception(res)
        res = re.sub(
            r'{\\"\$numberLong\\": \\"\d+\\"}',
            lambda m: re.search(r"\d+", m.group()).group(),
            res.decode("utf-8"),
        )
        data = json.loads(res)
        data_list = data["data"]
        res_list = []
        if data_list:
            for data in data_list:
                res_list.append(json.loads(data))
        res_df = pd.DataFrame(res_list)
        return res_df

    @staticmethod
    def es_query(das_url, post_data):
        """
        sql语句 查询 elasticsearch 库
        :param das_url: das_http_url
        :param post_data: {
            "sql": sql,                     # sql语句
            "engine": 1,                    # es引擎版本 1：官方 2: open distro
            "search_from": search_from,     # 分页查询offset 最大5w
            "fetch_size": fetch_size        # 单次查询总行数
        }
        :return:
        """
        b_ok, res = DasApi._post(das_url, "das/es/query", post_data=post_data)
        if not b_ok:
            raise Exception(res)
        engine = post_data.get("engine", 0)
        use_search = post_data.get("search_from", -1) >= 0
        data = json.loads(res)

        if engine == 0:
            # opendistro
            col_dict_lst = data["schema"]
            data_rows = data["datarows"]
            # total = data["total"]
            # size = data["size"]
            # status = data["status"]
        else:
            # origin
            if use_search:
                data_rows = data["map_rows"]
                return pd.DataFrame(data_rows)
            col_dict_lst = data["columns"]
            data_rows = data["rows"]
        df_cols = [col_dict["name"] for col_dict in col_dict_lst]

        if not data_rows:
            return pd.DataFrame(columns=df_cols)
        res_df = pd.DataFrame(np.array(data_rows), columns=df_cols)
        return res_df

    @staticmethod
    def es_insert(das_url, post_data):
        """
        elasticsearch 数据插入
        :param das_url: das_http_url
        :param post_data = {
            "kafka_addr": kafka_addr,   # kafka地址
            "topic": topic,             # kafka Topic
            "data_rows": data_rows      # 数据行
        }
        :return:
        """
        b_ok, res = DasApi._post(das_url, "das/es/insert", post_data=post_data)
        if not b_ok:
            raise Exception(res)
        return res

    @staticmethod
    def ch_query(das_url, post_data):
        """
        sql语句 查询 clickhouse 库
        :param das_url: das_http_url
        :param post_data: {
            "sql": sql,                     # sql语句
        }
        :return:
        """
        b_ok, res = DasApi._post(das_url, "/das/ch/query", post_data=post_data)
        if not b_ok:
            raise Exception(res)
        data = json.loads(res)

        res_df = pd.DataFrame(data["datarows"], columns=data["columns"])
        return res_df

    @staticmethod
    def ch_execute(das_url, post_data):
        """
        clickhouse 执行 sql (数据插入)
        :param das_url: das_http_url
        :param post_data: {
            "sql": sql,                     # sql语句
        }
        :return:
        """
        b_ok, res = DasApi._post(das_url, "/das/ch/query", post_data=post_data)
        if not b_ok:
            raise Exception(res)
        return b_ok


# if __name__ == '__main__':
# post_type = "das/mgo/query"
# post_data_ = dict()
# post_data_['js_sql'] = 'db.getSiblingDB("fumo_test").getCollection("player").find({})'
# post_data_['server'] = 'test'
#
# # DasApi.post(post_type=post_type, post_data=post_data)
# res_ = DasApi.mongo_query(post_data_)
#
# post_data_ = dict()
# post_data_['sql'] = 'SELECT * FROM log_money LIMIT 1'
# post_data_['engine'] = 1
# res_ = DasApi.es_query(post_data_)

# post_data = dict()
# post_data['sql'] = 'select * from main_test.log_player_op limit 10;'
# res_ = DasApi.ch_query(post_data)
#
# print (res_)
