# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/18 19:43:29
# @Software : python3.11
# @Desc     : TODO
import json

from redis import AuthenticationError
from yyxx_game_pkg.helpers.op_helper import OPHelper
from yyxx_game_pkg.utils.xstring import parse_json


class Operator(OPHelper):
    @classmethod
    def get_key(cls, operator, game_channel_id):
        redis = cls.redis()
        mp = cls.mp()
        try:
            cache_key = "api_operator_channel_%s_%s_key" % (
                operator,
                game_channel_id,
            )
            package = {}
            subpackage = {}

            sdk_data = redis.get_data(cache_key)

            if not sdk_data:
                sdk_data = {}
                sql = """
                    SELECT
                        t1.alias as operator, t2.game_channel_id, t2.group_id, t2.iw_id, t2.sdk_config, t3.alias as iw_alias
                    FROM
                        svr_operator t1, svr_channel t2 left join svr_inter_working_group t3 on t2.iw_id = t3.id
                    WHERE
                        ((t1.alias = '%s' AND t2.game_channel_id = '%s') OR (t1.alias = '%s' AND t2.game_channel_id='0'))
                    AND t1.oid = t2.oid
                    ORDER BY t2.id
                    DESC
                """ % (
                    operator,
                    game_channel_id,
                    operator,
                )
                data = mp.get_all(sql, cls.connection())

                if data:
                    for item in data:
                        if (
                            item["game_channel_id"] == "0"
                            or item["game_channel_id"] == 0
                        ):
                            # 母包配置
                            package = item
                        else:
                            # 分包配置
                            subpackage = item

                    if subpackage.get("sdk_config", "") or package.get(
                        "sdk_config", ""
                    ):
                        sdk_data["operator"] = (
                            subpackage["operator"]
                            if subpackage.get("operator", "")
                            else package.get("operator", "")
                        )
                        sdk_data["game_channel_id"] = (
                            subpackage["game_channel_id"]
                            if subpackage.get("game_channel_id", "")
                            else package.get("game_channel_id", "")
                        )
                        sdk_data["group_id"] = (
                            subpackage["group_id"]
                            if subpackage.get("group_id", "")
                            else package.get("group_id", "")
                        )
                        sdk_data["iw_id"] = (
                            subpackage["iw_id"]
                            if subpackage.get("iw_id", "")
                            else package.get("iw_id", "")
                        )
                        sdk_data["iw_alias"] = (
                            subpackage["iw_alias"]
                            if subpackage.get("iw_alias", "")
                            else package.get("iw_alias", "")
                        )

                        try:
                            if subpackage.get("sdk_config", ""):
                                sdk_subpackage = json.loads(
                                    subpackage.get("sdk_config", "{}")
                                )
                                sdk_package = json.loads(
                                    package.get("sdk_config", "{}")
                                )

                                for index, ist in sdk_subpackage.items():
                                    if sdk_subpackage.get(index, ""):
                                        sdk_package[index] = sdk_subpackage.get(
                                            index, ""
                                        )

                                subpackage["sdk_config"] = json.dumps(sdk_package)
                        except (TypeError, json.decoder.JSONDecodeError):
                            subpackage["sdk_config"] = {}

                        sdk_config = (
                            subpackage["sdk_config"]
                            if subpackage.get("sdk_config", "")
                            else package.get("sdk_config", "")
                        )
                        sdk_config = parse_json(sdk_config) if sdk_config else {}

                        sdk_data.update(sdk_config)
                        redis.set_data(cache_key, json.dumps(sdk_data))
                    else:
                        sdk_data = {}
                else:
                    sdk_data = {}
            else:
                sdk_data = parse_json(sdk_data)
            return sdk_data
        except AuthenticationError:
            return {}
        except Exception as e:
            print(e, type(e))
            return {}
