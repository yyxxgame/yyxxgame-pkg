# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/05/18 14:21:24
# @Software : python3.11
# @Desc     : TODO
from yyxx_game_pkg.center_api.model.TableFieldConf import TableFieldConf
from yyxx_game_pkg.helpers.op_helper import OPHelper
from yyxx_game_pkg.utils.xstring import parse_json


class OperatorServer(OPHelper):
    # 服务器数据
    @classmethod
    def get_oid_data(cls, receive_oid, receive_gcid, is_filter=True):
        cache_key = f"api_serverData_{receive_oid}_{receive_gcid}_OidData"

        sql = """
            SELECT
                t1.game_config
            FROM
                svr_channel t1,
                svr_operator t2
            WHERE
                t2.oid = t1.oid
            AND
                t2.alias = '{}'
            AND
                t1.game_channel_id = '{}'
        """.format(
            receive_oid, receive_gcid
        )
        # data = cls.cache(sql, cls.sql_get_one(), keyname)
        cache_data = cls.redis().get_data(cache_key)
        if not cache_data:
            data = cls.mp().get_one(sql, cls.connection())
            if data:
                cache_data = data["game_config"]
            else:
                cache_data = "{}"
            cls.redis().set_data(cache_key, cache_data)

        res = parse_json(cache_data)
        if not res or not isinstance(res, dict):
            res = {}

        if is_filter:
            res = TableFieldConf.filter_table_config("svr_channel", "game_config", res)

        return res
