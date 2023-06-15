# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/18 15:42:33
# @Software : python3.11
# @Desc     : map_core
import json
import time
from abc import abstractmethod

from flask import request
from yyxx_game_pkg.center_api.model.Operator import Operator
from yyxx_game_pkg.center_api.model.OperatorServer import OperatorServer
from yyxx_game_pkg.conf import settings
from yyxx_game_pkg.crypto.basic import RANDOM_STRING_CHARS_LOWER, get_random_string, md5
from yyxx_game_pkg.crypto.make_sign import make_sign
from yyxx_game_pkg.helpers.op_helper import OPHelper


class MapCore(OPHelper):
    Flag = "sign"
    Time = "time"
    Gmip = None
    Imei = None
    Callback = None
    OutTime = 0

    make_sign_exclude = {"gmip", "cp_platform", "ch_conter", "opts"}
    API_KEY = settings.API_KEY
    params = None
    _plat_code = None
    _operator = None
    _game_channel_id = None

    # 大额充值限制
    max_money_limit = 5000

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def init_ip_imei(self, values):
        self.Gmip = values.get("gmip", "")
        self.Imei = values.get("imei", "")

    def get_params(self, data):
        return data

    def get_params_helper(self, data, data_ary) -> None:
        pass

    def check_sign(self, values):
        sign = values.get(self.Flag, None)
        if sign is None:
            return False
        _sign = self.make_sign(values)
        if sign != _sign:
            return False
        return True

    def make_sign(self, values) -> str:
        return make_sign(
            values, self.api_key, exclude=self.make_sign_exclude, time_key=self.Time
        )

    def channel_make_sign(self, values, sign_key) -> str:
        return make_sign(
            values, sign_key, exclude=self.make_sign_exclude, time_key=None
        )

    def check_time_out(self, values):
        _time = int(values.get(self.Time, 0))
        t = time.time()
        if self.OutTime != 0 and int(t) - _time > self.OutTime:
            return False
        return True

    def check_public(self, values) -> bool:
        return True

    def sdk_rechfeed(self, error_code, msg="") -> dict:
        if not msg:
            msg = str(error_code.get("msg", ""))
        code = int(error_code.get("code", 0))
        return {"ret": code, "msg": msg}

    def feedback(
        self, error_code, msg_data: dict | list = None, msg="", *args, **kwargs
    ):
        if type(error_code) == dict:
            if not msg:
                msg = str(error_code.get("msg", ""))
            code = int(error_code.get("code", 0))
        else:
            code = error_code

        result = {
            f"{get_random_string(5, RANDOM_STRING_CHARS_LOWER)}_myzd_a": str(
                int(time.time())
            ),
            f"{get_random_string(5, RANDOM_STRING_CHARS_LOWER)}_myzd_b": str(
                int(time.time())
            ),
            "server_time": int(time.time()),
        }
        if msg_data or msg_data == 0:
            receive_data = request.values
            receive_path = request.path
            receive_oid = receive_data.get("oid", "")
            receive_gcid = receive_data.get("gcid", "")
            receive_action = ""
            if not receive_gcid:
                receive_gcid = receive_data.get("game_channel_id", "")

            receive_path_list = receive_path.split("/")
            if receive_oid and receive_gcid:
                if len(receive_path_list) > 2:
                    receive_action = receive_path_list[2]
                else:
                    receive_action = receive_path_list[1]

                oid_data = OperatorServer.get_oid_data(receive_oid, receive_gcid)

                if oid_data.get("is_close_check", None):
                    result["close_check"] = "yesyes"

            data_str = json.dumps(msg_data)
            data_str = "\\/".join(data_str.split("/"))
            data_sign = md5(f"{data_str}{receive_action}{self.API_KEY}")

            result["code"] = code
            result["msg"] = msg
            result["data"] = msg_data
            result["data_sign"] = data_sign

            result = "\\\n".join(json.dumps(result, ensure_ascii=False).split("\n"))
        else:
            result = json.dumps({"code": code, "msg": msg}, ensure_ascii=False)

        if self.Callback:
            result = "{}({})".format(self.Callback, result)

        return result

    def is_open_ip(self, gmip=""):
        pass

    @property
    def operator(self):
        return Operator

    @property
    def api_key(self):
        print(self.API_KEY)
        if self.API_KEY is None:
            raise ValueError("API_KEY must be specified")
        return self.API_KEY


class MapCoreMinix:
    def get_params(self, data):
        data_ary = {
            "cp_platform": data.get("cp_platform", ""),
            "page_size": 10000,
            "page": 1,
        }

        self.get_params_helper(data, data_ary)

        return data_ary

    def make_sign(self, values):
        sdk_data = self.operator.get_key(self._plat_code, self._game_channel_id)
        pay_key = sdk_data.get("pay_key", "")
        return self.channel_make_sign(values, pay_key)

    @abstractmethod
    def get_params_helper(self, data, data_ary) -> None:
        """
        补充数据
        for k, v in self.params.items():
            if v:
                data_ary[k] = data.get(v, "")
        """

    @abstractmethod
    def feedback_helper(self, data_list, error_code, ex=None):
        """
        if data_list:
            code = 1
            message = "success"
        else:
            code = 2
            message = error_code.get("msg", "")

        return {"code": code, "message": message, "data": data_list}
        """
