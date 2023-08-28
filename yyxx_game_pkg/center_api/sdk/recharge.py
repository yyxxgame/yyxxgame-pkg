# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/18 16:02:34
# @Software : python3.11
# @Desc     : 充值回调
from abc import ABC, abstractmethod
from dataclasses import dataclass

from yyxx_game_pkg.center_api.sdk.map_core import MapCore
from yyxx_game_pkg.conf import settings


@dataclass
class Params:
    """
    @param extra: 拓参
    @param cp_order_id: 厂商订单ID, 由厂商生成
    @param channel_order_id: 渠道方订单ID
    @param player_id: 角色ID
    @param is_check_username: 是否验证帐号与玩家ID
    @param channel_username: 渠道帐号
    @param is_test: 是否测试订单
    """
    extra: str = "extra"
    cp_order_id: str = "billno"
    channel_order_id: str = "order_id"
    player_id: str = "role_id"
    channel_username: str = "openid"
    money: str = "amount"
    is_check_username: int = 1
    is_test: int = 0


class BaseRecharge(MapCore, ABC):
    """
    注意：
        方法 modify_params 用来修改 params 的参数值
        需要实现 get_params_handler feedback 方法
        get_params_handler 是对 get_params 参数的补充
        feedback
    """

    params = Params()

    def modify_params(self):
        """
        修改 self.params 属性
        """
        pass

    def get_params(self, data) -> dict:
        self.modify_params()
        extra = data.get(self.params.extra, "")
        if not extra:
            return {}

        ext_ary = extra.split(",")
        data_ary = {"extra": extra}
        self.get_params_core(data, data_ary, ext_ary)
        self.get_params_helper(data, data_ary)

        return data_ary

    def get_params_core(self, data, data_ary, ext_ary):
        data_ary["cp_order_id"] = data.get(self.params.cp_order_id, "")
        data_ary["channel_order_id"] = data.get(self.params.channel_order_id, "")
        data_ary["player_id"] = data.get(self.params.player_id)
        data_ary["is_check_username"] = self.params.is_check_username
        data_ary["channel_username"] = data.get(self.params.channel_username, "")
        if len(ext_ary) > 5:
            data_ary["recharge_id"] = int(ext_ary[5])

    def get_params_helper(self, data, data_ary) -> None:
        """
        补充数据, 添加额外参数
        对 get_params 中 data_ary 数据的补充
        无法在 get_params_core 中通过通用方式获得的参数，在此处进行处理
        --------------------------------
        money  金额
        real_money  实付金额
        extra_gold  赠送元宝（渠道返利）
        extra_gold_bind  赠送绑元（渠道返利）
        pay_dt 充值时间（秒）
        --------------------------------
        """
        amount = int(data.get(self.params.money, 0))
        data_ary["real_money"] = int(amount / 100)
        data_ary["money"] = amount / 100

    def make_sign_helper(self, values) -> (dict, str):
        ext_ary = values[self.params.extra].split(",")
        plat_code = ext_ary[0]
        game_channel_id = ext_ary[1]
        sdk_data = self.operator.get_key(plat_code, game_channel_id)
        pay_key = sdk_data.get("pay_key", "")
        return values, pay_key

    def make_sign(self, values) -> str:
        values, pay_key = self.make_sign_helper(values)
        return self.channel_make_sign(values, pay_key)

    @abstractmethod
    def feedback(self, error_code, data: dict = None, msg="", *args, **kwargs):
        """
        根据需求 return 相应的数据
        """
        return error_code
