# -*- coding: utf-8 -*-
# @Author   : {{ cookiecutter.author }}
# @Time     : {{ cookiecutter.timestamp }}
# @Software : {{ cookiecutter.python_version }}
# @Desc     : TODO
from yyxx_game_pkg.center_api.sdk.recharge import BaseRecharge

from .map_factor import MapRecharge


class Recharge(MapRecharge, BaseRecharge):
    """
    类属性默认值
    @param extra_key = "extra"
    @param cp_order_id_key = None
    @param order_id_key = "orderId"
    @param platform_order_id_key = "orderId"
    @param product_type = "coin"

    按需修改
    """

    # 父类中核心代码，此处可删除
    # def get_params(self, data) -> dict:
    #     extra = data.get(self.extra_key, "")
    #     if not extra:
    #         return {}
    #
    #     ext_ary = extra.split(",")
    #     data_ary = {"extra": extra}
    #     self.get_params_core(data, data_ary, ext_ary)
    #     self.get_params_helper(data, data_ary)
    #
    #     return data_ary

    # 项目通用方法，一般不需要修改，直接使用父类方法，此处可删除
    def get_params_core(self, data, data_ary, ext_ary) -> None:
        """
        --------------------------------
        默认获取以下数据
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
        data_ary["platformOrderId"] = data.get(self.platform_order_id_key, "")  # 渠道方订单ID（C表要用）
        if len(ext_ary) > 6:
            data_ary["recharge_id"] = int(ext_ary[5])
        data_ary["productType"] = self.product_type
        data_ary["productID"] = ""
        --------------------------------
        """
        super().get_params_core(data, data_ary, ext_ary)

    def get_params_helper(self, data, data_ary) -> None:
        """
        对 get_params 中 data_ary 数据的补充
        无法在 get_params_core 中通过通用方式获得的参数，在此处进行处理
        --------------------------------
        e.g. currency promotion extraGoldBindProportion extraGoldBind
        data_ary["currency"] = data.get("currency", "")
        data_ary["promotion"] = ""
        data_ary["extraGoldBindProportion"] = ""
        data_ary["extraGoldBind"] = ""
        --------------------------------
        """

    def make_sign_helper(self, values) -> (dict, str):
        """
        ext_ary = values[self.extra_key].split(",")
        plat_code = ext_ary[0]
        game_channel_id = ext_ary[1]
        sdk_data = self.operator.get_key(plat_code, game_channel_id)
        pay_key = sdk_data.get("pay_key", "")
        return values, pay_key

        :param values:
        :return: values, pay_key

        --------------------------------
        如果对 values 或 pay_key 有调整，在此处修改
        values, pay_key = super().make_sign_helper(values)
        ... (具体修改过程)
        return values, pay_key
        --------------------------------
        """
        return super().make_sign_helper(values)

    # 签名核心方法，此处可删除
    # def make_sign(self, values, sign_key=None) -> str:
    #     values, pay_key = self.make_sign_helper(values)
    #     return self.channel_make_sign(values, sign_key)

    def channel_make_sign(self, values, sign_key=None) -> str:
        """
        默认签名方式为  md5(yyxx_game_pkg.crypto.basic.md5)
            post_data 中的键按照首字母升序排列

        也可继承或重新 MapRecharge MapFactor 中的方法

        :return: 签名字符串
        """
        return super().channel_make_sign(values, sign_key)

    def feedback(self, error_code, data: dict = None, msg="", *args, **kwargs):
        """
        根据需求 return 相应的数据
        """
        return error_code
