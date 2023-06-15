# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/18 16:36:36
# @Software : python3.11
# @Desc     : make_sign
from typing import Iterable

from yyxx_game_pkg.crypto.basic import md5


def make_sign(
    values: dict,
    secret_key: str,
    *,
    exclude: Iterable = None,
    time_key="time",
    make_sign_func=md5,
    make_sign_key: str = None,
    digest_mod=None,
) -> str:
    """
    签名方法
    :param values: 需要加密的数据（字典）
    :param secret_key: 加密秘钥
    :param exclude: 字段名可选列表，如果提供，加密时会排除其中字段，然后进行加密
    :param time_key: 获取时间戳的字段名；默认为 time
    :param make_sign_func: 进行加密的方法
    :param make_sign_key: 加密使用的秘钥（针对使用hmac的加密方法）
    :param digest_mod: 加密使用的方法（针对使用hmac的加密方法），可以为 hashlib.sha1 或 "SHA1" 等等
    """
    if exclude is None:
        exclude = []

    string = ""
    for key in sorted(values):
        if key not in exclude:
            string += f"{key}={values[key]}&"

    _time = values.get(time_key, "")
    if _time:
        raw_str = f"{string}time={_time}{secret_key}"
    else:
        raw_str = f"{string[:-1]}{secret_key}"

    return make_sign_func(raw_str, make_sign_key, digest_mod)
