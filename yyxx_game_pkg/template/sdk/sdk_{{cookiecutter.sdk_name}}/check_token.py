# -*- coding: utf-8 -*-
# @Author   : {{ cookiecutter.author }}
# @Time     : {{ cookiecutter.timestamp }}
# @Software : {{ cookiecutter.python_version }}
# @Desc     : TODO
import time

from yyxx_game_pkg.center_api.sdk.check_token import BaseCheckToken
from yyxx_game_pkg.utils.error_code import ErrorCode

from .map_factor import MapFactor


class Check_Token(MapFactor, BaseCheckToken):
    # is_https = True
    # method = "POST"
    # time_param = ("time", int(time.time())

    # 根据接口文档填写 params 的键值
    # params key: post_data的键
    # params value: kwargs的键
    # --> post_data[key] = kwargs[value]
    params = {}
    sdk_exclude = ()

    # 父类中核心代码，此处可删除
    # def run_check_token(self, *args, **kwargs) -> dict:
    #     """
    #     run check token
    #     """
    #     sdk_helper, response_helper = self.sdk_version_choice(**kwargs)
    #     if sdk_helper is None:
    #         return self.sdk_rechfeed(ErrorCode.ERROR_INVALID_PARAM)
    #
    #     channel_data, post_data = sdk_helper(**kwargs)
    #     response = self.sdk_check_token(channel_data, post_data)
    #
    #     return response_helper(response, **kwargs)

    def sdk_helper(self, sdk_exclude=(), **kwargs) -> (dict, dict):
        """
        channel_data = kwargs.get("channel_data", {})

        post_data = {}
        for k, v in self._params.items():
            post_data[k] = kwargs.get(v)
        if self.Time not in sdk_exclude:
            post_data[self.Time] = int(time.time())
        if self.Flag not in sdk_exclude:
            post_data[self.Flag] = self.channel_make_sign(
                post_data, channel_data.get("app_key", "")
            )

        return channel_data, post_data

        :param sdk_exclude: exclude parameters
        :param kwargs: 参数
        :return: channel_data, post_data

        --------------------------------
        如果 post_data 有修改或者补充，可以在此方法中添加
        channel_data, post_data = super().sdk_helper(**kwargs)
        post_data["需要修改或添加的键"] = "需要修改或添加的值"
        return channel_data, post_data
        --------------------------------
        """
        return super().sdk_helper(**kwargs)

    def channel_make_sign(self, values, sign_key) -> str:
        """
        在sdk_helper中，如果只是 签名 的方法需要修改，
        可以在此方法中重写
        :param values: sdk_helper 中的 post_data
        :param sign_key: sdk_helper 中的 channel_data.get("app_key", "")
        :return: 签名字符串
        """
        return super().channel_make_sign(values, sign_key)

    def sdk_check_token(self, channel_data, post_data):
        """
        默认使用 登录验证URL进行二次验证

        如果不是使用登录验证URL的方式进行二次验证
        重写此方法进行验证
        同时，可以删除 sdk_helper 和 channel_make_sign

        return 的值在 response_helper 中使用
        具体返回什么视情况而定
        """
        return super().sdk_check_token(channel_data, post_data)

    def response_helper(self, response: dict, **kwargs) -> dict:
        """
        返回数据
        根据渠道文档，设置返回数据
        """
        if response and response["code"] == 0:
            data = {
                # ----- ret,user_id为必传参数 ------
                "ret": 1,
                "user_id": kwargs["?"],  # ? 值根据具体参数填写
                # --------------------------------
                # 如果还有其他参数, 按需添加
            }
            return data

        return super().response_helper(response, **kwargs)

    # sdk 版本映射，一般不需要改变，此处可删除
    # @property
    # def sdk_version_map(self) -> dict:
    #     """
    #     sdk version map
    #     如果存在多个version版本，需要添加对应的版本映射
    #     """
    #     return super().sdk_version_map
