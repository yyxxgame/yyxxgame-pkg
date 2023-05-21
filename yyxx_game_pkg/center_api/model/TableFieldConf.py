# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/05/18 14:35:56
# @Software : python3.11
# @Desc     : TODO
import json
import time

from yyxx_game_pkg.helpers.op_helper import OPHelper
from yyxx_game_pkg.utils.xstring import parse_json


class TableFieldConf(OPHelper):
    @classmethod
    def get_field_config_by_table(cls, table_name):
        result = {}
        cache_key = f"sys_table_field_config_{table_name}"
        sql = """
            SELECT
                *
            FROM
                sys_table_field_config
            WHERE
                table_name='{}'
        """.format(
            table_name
        )
        data = cls.cache(sql, cls.sql_func_get_one(), cache_key)
        if data:
            for value in data:
                result[value["field_name"]] = value

        return result

    @classmethod
    def filter_table_config(cls, table_name, field_name, filter_data):
        """
        过滤 filter_data 的值，如果有表字段配置，必须 在表字段配置中
        :param table_name:
        :param field_name:
        :param filter_data:
        :return:
        """
        if not table_name:
            return filter_data

        cache_data = cls.get_field_config_by_table(table_name)
        if not cache_data:
            return filter_data
        if isinstance(cache_data, dict):
            field_data = cache_data.get(field_name, None)
            if field_data is None:
                return filter_data
            field_config = field_data.get("field_config", "{}")
            res = parse_json(field_config)
            if not res:
                return {}
            result = {}
            df_time = int(time.time())
            df_json = json.dumps({})
            for key, val in res.items():
                fdv = filter_data.get(key, None)
                if fdv is None:
                    val_d = val.get("default", "")
                    val_t = val.get("type", "")

                    if val_t == "int":
                        val_d = int(val_d)
                    elif val_t == "json" or val_t == "jsons":
                        val_d = df_json
                    elif val_t == "time":
                        val_d = df_time
                    elif val_t == "times":
                        val_d = [df_time, df_time]
                    elif val_t == "switch":
                        val_d = 0
                    else:
                        val_d = 0
                    fdv = val_d
                result[key] = fdv
            return result
        else:
            return filter_data
