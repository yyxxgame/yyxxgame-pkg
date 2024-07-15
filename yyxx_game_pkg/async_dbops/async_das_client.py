# -*- coding: utf-8 -*-
"""
@File: async_das_client.py
@Author: ltw
@Time: 2023/6/14

das_api python 协程异步调用
"""

import httpx
import numpy as np
import pandas as pd
import ujson as json
from yyxx_game_pkg.utils.dtypes import trans_unsupported_types


class AsyncDasClient:
    """
    AioDasClient py
    """

    async def _post(self, das_url, post_type, post_data):
        url = f"{das_url}/{post_type}"
        post_data = trans_unsupported_types(post_data)
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=post_data, timeout=600)
            return response.is_success, response.content

    async def es_query(self, das_url, post_data):
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
        b_ok, res = await self._post(das_url, "das/es/queryx", post_data=post_data)
        if not b_ok:
            raise RuntimeError(f"res:{res} \n post_data:{post_data}")
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

    async def es_insert(self, das_url, post_data):
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
        b_ok, res = await self._post(das_url, "das/es/insert", post_data=post_data)
        if not b_ok:
            raise RuntimeError(f"res:{res} \n post_data:{post_data}")
        return res

    async def ch_query(self, das_url, post_data):
        """
        sql语句 查询 clickhouse 库
        :param das_url: das_http_url
        :param post_data: {
            "sql": sql,                     # sql语句
        }
        :return:
        """
        b_ok, res = await self._post(das_url, "/das/ch/queryx", post_data=post_data)
        if not b_ok:
            raise RuntimeError(f"res:{res} \n post_data:{post_data}")
        data = json.loads(res)

        res_df = pd.DataFrame(data["datarows"], columns=data["columns"])
        return res_df

    async def ch_execute(self, das_url, post_data):
        """
        clickhouse 执行 sql (数据插入)
        :param das_url: das_http_url
        :param post_data: {
            "sql": sql,                     # sql语句
        }
        :return:
        """
        b_ok, res = await self._post(das_url, "/das/ch/exec", post_data=post_data)
        if not b_ok:
            raise RuntimeError(f"res:{res} \n post_data:{post_data}")
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
