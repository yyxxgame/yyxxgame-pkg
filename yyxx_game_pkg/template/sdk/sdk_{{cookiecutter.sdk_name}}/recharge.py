# -*- coding: utf-8 -*-
# @Author   : {{ cookiecutter.author }}
# @Time     : {{ cookiecutter.timestamp }}
# @Software : {{ cookiecutter.python_version }}
# @Desc     : TODO
from yyxx_game_pkg.center_api.sdk.recharge import BaseRecharge

from .map_factor import MapRecharge


class Recharge(MapRecharge, BaseRecharge):
    # 父类中核心代码，此处可删除
    # def get_params(self, data) -> dict:
    #     self.modify_params()
    #     extra = data.get(self.params.extra, "")
    #     if not extra:
    #         return {}
    #
    #     ext_ary = extra.split(",")
    #     data_ary = {"extra": extra}
    #     self.get_params_core(data, data_ary, ext_ary)
    #     self.get_params_helper(data, data_ary)
    #
    #     return data_ary

    def modify_params(self):
        """
        修改 self.params 属性
        默认值:
            extra: str = "extra"
            cp_order_id: str = "billno"
            channel_order_id: str = "order_id"
            player_id: str = "role_id"
            channel_username: str = "openid"
            is_check_username: int = 1
            is_test: int = 0

        self.params.cp_order_id = "xxx"
        """
        pass

    # 项目通用方法，一般不需要修改，直接使用父类方法，此处可删除
    def get_params_core(self, data, data_ary, ext_ary) -> None:
        """
        --------------------------------
        默认获取以下数据
        data_ary["cp_order_id"] = data.get(self.params.cp_order_id, "")
        data_ary["channel_order_id"] = data.get(self.params.channel_order_id, "")
        data_ary["player_id"] = data.get(self.params.player_id)
        data_ary["is_check_username"] = self.params.is_check_username
        data_ary["channel_username"] = data.get(self.params.channel_username, "")
        if len(ext_ary) > 6:
            data_ary["recharge_id"] = int(ext_ary[5])
        --------------------------------
        """
        super().get_params_core(data, data_ary, ext_ary)

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
        super().get_params_helper(data, data_ary)

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
    #     return self.channel_make_sign(values, pay_key)

    def channel_make_sign(self, values, sign_key) -> str:
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
