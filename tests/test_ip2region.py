# -*- coding: utf-8 -*-
"""
@File: test_ip2region
@Author: ltw
@Time: 2023/3/10
"""
from yyxx_game_pkg.ip2region import ip_x


if __name__ == '__main__':
    print(ip_x.ip2region("113.52.123.156"))
    # 中国|0|澳门|0|澳门电讯
