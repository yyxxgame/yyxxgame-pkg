# -*- coding: utf-8 -*-
"""
@File: ip_x
@Author: ltw
@Time: 2022/12/27
"""
import os
from yyxx_game_pkg.ip2region.xdbSearcher import XdbSearcher


# 1. 缓存
dbPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ip2region.xdb")
cb = XdbSearcher.loadContentFromFile(dbfile=dbPath)


def ip2region(target_ip):
    """
    ip 获取地区
    :param target_ip:
    :return:
    """

    # 2. 创建查询对象
    searcher = XdbSearcher(contentBuff=cb)

    # 3. 执行查询
    # ip = "1.2.3.4"
    region_str = searcher.searchByIPStr(target_ip)

    searcher.close()
    return region_str
