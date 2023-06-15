# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/18 16:17:00
# @Software : python3.11
# @Desc     : 二次认证
import time
from abc import ABC, abstractmethod
from typing import Callable, NewType
from urllib.parse import unquote

from yyxx_game_pkg.center_api.sdk.map_core import MapCore
from yyxx_game_pkg.utils.error_code import ErrorCode
from yyxx_game_pkg.utils.xhttp import http_request
from yyxx_game_pkg.utils.xstring import parse_json

SDK_HELPER = NewType("SDK_HELPER", Callable[[...], None])
RESPONSE_HELPER = NewType("RESPONSE_HELPER", Callable[[...], None])


class BaseCheckToken(MapCore, ABC):
    """
    注意：需要实现 response_helper 方法

    @func response_helper: 处理返回数据
    @func sdk_check_token: 验证token方法
    @func sdk_helper: sdk 参数处理
    @func channel_make_sign: 默认 sorted(params) md5

    根据渠道需求填写以下参数
    @param is_https: 请求是否为https；默认 True
    @param method: 请求方式 POST GET；默认 POST
    @param params: (key)发送和(value)接收 参数的字段名
    """

    is_https = True  # True False
    method = "POST"
    # params = {}
    sdk_exclude = ()

    def run_check_token(self, *args, **kwargs) -> dict:
        """
        run check token
        """
        sdk_helper, response_helper = self.sdk_version_choice(**kwargs)
        if sdk_helper is None:
            return self.sdk_rechfeed(ErrorCode.ERROR_INVALID_PARAM)

        channel_data, post_data = sdk_helper(self.sdk_exclude, **kwargs)
        response = self.sdk_check_token(channel_data, post_data)

        return response_helper(response, **kwargs)

    @abstractmethod
    def response_helper(self, response: dict | None, **kwargs) -> dict:
        """
        根据需求 return 相应的数据
        :return: {"ret": 1, "user_id": "any_user_id"}
        """
        return self.sdk_rechfeed(ErrorCode.ERROR_INVALID_PARAM, "验证失败")

    @property
    def _params(self):
        """
        params = {
            "appId": "sdk_appId",
            "accountId": "sdk_accountId",
            "token": "sdk_token",
        }
        """
        if self.params is None:
            raise ValueError("params must be specified as a dict")

        return self.params

    def sdk_helper(self, sdk_exclude=(), **kwargs) -> (dict, dict):
        """
        处理 sdk 数据
        :param sdk_exclude: sdk_helper 处理数据，要排除的key
            可选值: time(self.Time) sign(self.Flag)
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

    def sdk_check_token(self, channel_data, post_data) -> dict | None:
        """
        处理方法不适用时，重写此方法
        默认使用发送请求的方式获取token验证结果
        """
        url = channel_data.get("api_url", "")
        if not url:
            return None

        result = http_request(
            url=url,
            data=post_data,
            is_https=self.is_https,
            method=self.method,
        )

        return parse_json(unquote(result))

    @property
    def sdk_version_map(self) -> dict:
        """
        sdk version map
        如果存在多个version版本，需要添加对应的版本映射
        """
        return {
            "1.0.0": {
                "sdk_helper": self.sdk_helper,
                "response_helper": self.response_helper,
            },
        }

    def sdk_version_choice(self, **kwargs) -> (SDK_HELPER, RESPONSE_HELPER):
        """
        匹配对应 sdk version 相关方法 sdk_handler response_helper
        """
        sdk_version = kwargs.get("sdk_version", "1.0.0")

        version_map = self.sdk_version_map.get(sdk_version, None)
        if version_map is None:
            return None, None

        sdk_helper = version_map["sdk_helper"]
        response_helper = version_map["response_helper"]

        return sdk_helper, response_helper
