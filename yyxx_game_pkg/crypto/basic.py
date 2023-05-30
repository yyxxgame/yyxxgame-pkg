# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/03/22 16:51:15
# @Software : python3.11
# @Desc     : 内置加密模块 -> 加密
import hashlib
import hmac
import secrets

RANDOM_STRING_CHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
RANDOM_STRING_CHARS_LOWER = "abcdefghijklmnopqrstuvwxyz"


def md5(raw_str: str, secret_key=None, digest_mod=None) -> str:
    """
    md5加密
    """
    cipher = hashlib.md5()
    cipher.update(raw_str.encode("utf-8"))
    return cipher.hexdigest()


def hmac_crypto(raw_str: str, secret_key: str, digest_mod=hashlib.sha1) -> str:
    """
    :param raw_str:
    :param secret_key:
    :param digest_mod: hashlib.sha1 hashlib.sha256 ...
    """
    hmac_code = hmac.new(
        key=secret_key.encode(), msg=raw_str.encode(), digestmod=digest_mod
    ).hexdigest()
    return hmac_code


def get_random_string(length: int, allowed_chars: str = RANDOM_STRING_CHARS) -> str:
    """
    Return a securely generated random string.
    返回随机字符串
    """
    return "".join(secrets.choice(allowed_chars) for i in range(length))
