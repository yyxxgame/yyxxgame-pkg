# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/03/22 16:56:11
# @Software : python3.11
# @Desc     : operator file 文件处理相关
import re


def filter_path(path: str) -> str:
    """
    过滤文件路径
    :param path:
    :return:
    """
    path = path.replace("..", "")
    path = path.replace("|", "")
    path = path.replace('"', "")
    return path


def get_file_size(val: str) -> int:
    """
    获取文件大小
    1t 1g 1m 1k 1b
    """
    rule = r"(^\d+(\.\d+)?)[tgmk]?b?$"
    val = val.lower()
    number = re.match(rule, val).group(1)

    rate = 1
    if val.find("t") != -1:
        rate = 1024 * 1024 * 1024 * 1024
    elif val.find("g") != -1:
        rate = 1024 * 1024 * 1024
    elif val.find("m") != -1:
        rate = 1024 * 1024
    elif val.find("k") != -1:
        rate = 1024
    return int(float(number) * rate)
