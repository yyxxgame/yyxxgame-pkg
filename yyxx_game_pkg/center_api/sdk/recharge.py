
# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/18 16:02:34
# @Software : python3.11
# @Desc     : 充值回调
from abc import ABC, abstractmethod

from yyxx_game_pkg.center_api.sdk.map_core import MapCore
from yyxx_game_pkg.conf import settings


class BaseRecharge(MapCore, ABC):
    """
    注意：需要实现 get_params_handler feedback 方法
        get_params_handler 是对 get_params 参数的补充
        feedback

    @param extra_key arguments
    @param cp_order_id_key:
    @param order_id_key:
    @param platform_order_id_key:
    @param product_type:
    """

    extra_key = "extra"
    cp_order_id_key = None
    order_id_key = "orderId"
    platform_order_id_key = "orderId"
    product_type = "coin"

    def get_params(self, data) -> dict:
        extra = data.get(self.extra_key, "")
        if not extra:
            return {}

        ext_ary = extra.split(",")
        data_ary = {"extra": extra}
        self.get_params_core(data, data_ary, ext_ary)
        self.get_params_helper(data, data_ary)

        return data_ary

    def get_params_core(self, data, data_ary, ext_ary):
        data_ary["cp_platform"] = data.get("cp_platform", "")
        data_ary["platCode"] = ext_ary[0]  # 渠道商
        data_ary["game_channel_id"] = ext_ary[1]  # 渠道ID
        data_ary["serverID"] = ext_ary[2]  # 服ID
        data_ary["roleID"] = ext_ary[3]  # 角色ID
        data_ary["cpOrderID"] = (
            ext_ary[4]
            if self.cp_order_id_key is None
            else data.get(self.cp_order_id_key, "")
        )  # 厂商订单ID，由厂商生成
        data_ary["orderID"] = data.get(self.order_id_key, "")  # 渠道方订单ID
        data_ary["platformOrderId"] = data.get(
            self.platform_order_id_key, ""
        )  # 渠道方订单 ID（C表要用）
        if len(ext_ary) > 6:
            data_ary["recharge_id"] = int(ext_ary[5])

        data_ary["productType"] = self.product_type
        data_ary["productID"] = ""

    def get_params_helper(self, data, data_ary) -> None:
        """
        补充数据, 添加额外参数
        对 get_params 中 data_ary 数据的补充
        无法在 get_params_core 中通过通用方式获得的参数，在此处进行处理
        """

    def make_sign_helper(self, values) -> (dict, str):
        ext_ary = values[self.extra_key].split(",")
        plat_code = ext_ary[0]
        game_channel_id = ext_ary[1]
        sdk_data = self.operator.get_key(plat_code, game_channel_id)
        pay_key = sdk_data.get("pay_key", "")
        return values, pay_key

    def make_sign(self, values, sign_key=None) -> str:
        values, pay_key = self.make_sign_helper(values)
        return self.channel_make_sign(values, sign_key)

    @abstractmethod
    def feedback(self, error_code, data: dict = None, msg="", *args, **kwargs):
        """
        根据需求 return 相应的数据
        """
        return error_code
