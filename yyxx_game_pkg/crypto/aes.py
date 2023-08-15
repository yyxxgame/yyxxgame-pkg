# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/03/28 10:44:11
# @Software : python3.11
# @Desc     : AES encryption AES 加密
import json

from SecureHTTP import AESDecrypt, AESEncrypt

from yyxx_game_pkg.conf import settings
from yyxx_game_pkg.logger.log import root_log


def encryption_deal_with(data, _type="D"):
    key = settings.ENCRTPTION_KEY
    try:
        if _type == "D":
            aes_data = AESDecrypt(key, data, input="hex")
            aes_data = str(aes_data, encoding="utf-8")
            try:
                data = json.loads(aes_data[5:])
            except Exception as e:
                aes_data = aes_data.replace("\\", "\\\\")
                data = json.loads(aes_data[5:], strict=False)
                root_log(f"json解析错误: {aes_data}, {e}", level="error")
        elif _type == "E":
            data = AESEncrypt(key, data, output="hex")
    except Exception as e:
        root_log(f"type: {_type}, 错误: {e}", level="error")
    return data
