# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/13 17:28:50
# @Software : python3.11
# @Desc     : string
import json


def pascalize(snake: str) -> str:
    """
    Converts a string: snake_case to PascalCase
    """
    pascal = "".join(map(lambda x: x.capitalize(), snake.split("_")))
    return pascal


def parse_json(json_str) -> dict:
    """
    解析json字符串
    :param json_str:
    :return:
    """
    try:
        result = json.loads(json_str)
        return result
    except (TypeError, json.decoder.JSONDecodeError):
        return {}
