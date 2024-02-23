# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/03/28 10:44:11
# @Software : python3.11
# @Desc     : AES encryption AES 加密
import json
import re

from SecureHTTP import AESDecrypt, AESEncrypt

from yyxx_game_pkg.conf import settings
# from yyxx_game_pkg.logger.log import root_log


def remove_numeric_prefix(text):
    pattern = r"^\d+"
    return re.sub(pattern, "", text)


def encryption_deal_with(data, _type="D"):
    key = settings.ENCRTPTION_KEY
    try:
        if _type == "D":
            aes_data = AESDecrypt(key, data, input="hex")
            aes_data = str(aes_data, encoding="utf-8")
            if "{" in aes_data:
                aes_data = remove_numeric_prefix(aes_data)
            try:
                data = json.loads(aes_data)
            except Exception as e:
                aes_data = aes_data.replace("\\", "\\\\")
                data = json.loads(aes_data, strict=False)
                # root_log(f"json解析错误: {aes_data}, {e}", level="error")
        elif _type == "E":
            if isinstance(data, bytes):
                data = data.decode("utf-8")
            data = AESEncrypt(key, data, output="hex")
    except Exception as e:
        # root_log(f"type: {_type}, 错误: {e}", level="error")
        pass
    return data
