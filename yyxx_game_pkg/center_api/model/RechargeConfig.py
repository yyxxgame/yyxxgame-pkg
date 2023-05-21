# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/23 09:44:14
# @Software : python3.11
# @Desc     : TODO
import json

from yyxx_game_pkg.helpers.op_helper import OPHelper
from yyxx_game_pkg.utils.xstring import parse_json


class RechargeConfig(OPHelper):
    @classmethod
    def get_mapping_config(cls, oid="", gcid=""):
        try:
            sql = """
                SELECT
                    t1.id,
                    IFNULL(t4.json, '{}') json
                FROM
                    svr_channel t1
                LEFT JOIN svr_channel_group t2 ON t1.group_id = t2.id
                LEFT JOIN svr_operator t3 ON t1.oid = t3.oid
                LEFT JOIN api_recharge_mapping t4 ON t1.id = t4.channel_auto_id
                WHERE
                    t3.alias ='%s'
                AND t1.game_channel_id = '%s'
                ORDER BY
                    t1.id DESC
                """ % (
                oid,
                gcid,
            )
            result = cls.mp().get_one(sql, cls.connection())
            if result and result.get("json", ""):
                return parse_json(result["json"])
            return {}
        except:
            return False

    @classmethod
    def get_recharge_config(cls):
        try:
            sql = "SELECT * FROM api_recharge_config"
            res = cls.mp().get_all(sql, cls.connection())
            result = {}
            if res:
                for v in res:
                    vid = v["id"]
                    result[str(vid)] = v
            return result
        except:
            return {}

    @classmethod
    def get_check_recharge_config(cls, param_server_id):
        try:
            sql = (
                f"SELECT * FROM api_check_recharge_config where sid = {param_server_id}"
            )
            res = cls.mp().get_all(sql, cls.connection())
            result = {}
            if res:
                for v in res:
                    vid = v["recharge_id"]
                    result[str(vid)] = v
            return result
        except:
            return False

    @classmethod
    def recharge_config(cls):
        redis_key = "api_recharge_platform"
        recharge_config = cls.redis().get_data(redis_key)
        if not recharge_config:
            recharge_config = cls.get_recharge_config()
            if recharge_config:
                cls.redis().set_data(redis_key, json.dumps(recharge_config))
        if not isinstance(recharge_config, dict):
            recharge_config = json.loads(recharge_config)

        return recharge_config
