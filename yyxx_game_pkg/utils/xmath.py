# -*- coding: utf-8 -*-
"""
@File: xmath
@Author: ltw
@Time: 2022/9/27
"""


def cal_rate(top, bottom, precision=1, limit=100.0):
    """
    # 百分比i
    :param top: 分子
    :param bottom: 分母
    :param precision: 小数点
    :param limit: 是否限制100%
    :return:
    """
    if bottom == 0:
        return "0%"
    res = round(float(top) * 100 / bottom, precision)
    if precision == 0:
        res = int(res)
        limit = int(limit)
    if limit > 0:
        res = min(limit, res)
    return "{}%".format(res)


def compare_rate(val_a, val_b):
    """
    对比增长
    :param val_a:
    :param val_b:
    :return:
    """
    rate = cal_rate((val_a - val_b), val_b, limit=-1)
    return rate


def cal_round(top, bottom, precision=1):
    """
    # 除
    :param top: 分子
    :param bottom: 分母
    :param precision: 小数点
    :return:
    """
    if bottom == 0:
        return 0
    return round(float(top) / bottom, precision)
