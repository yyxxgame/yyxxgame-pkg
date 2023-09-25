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
    fmt = f"%0.{precision}f"
    return "{}%".format(fmt % res)


def compare_rate(val_a, val_b):
    """
    对比增长
    :param val_a:
    :param val_b:
    :return:
    """
    rate = cal_rate((val_a - val_b), val_b, limit=-1)
    return rate


def cal_round(top, bottom, precision=1, string=False):
    """
    # 除
    :param top: 分子
    :param bottom: 分母
    :param precision: 小数点
    :param string: 是否返回string
    :return:
    """
    if bottom == 0:
        return 0
    res = round(float(top) / bottom, precision)
    if string:
        fmt = f"%0.{precision}f"
        return fmt % res
    return res


class MergeContinuousNumber:
    """合并连续数字"""

    FILLKEY = "[FILLKEY]"

    @classmethod
    def parse_to_sql(cls, num_lst: list[int], key_name="", single_split_len=5, batch_num=0):
        from yyxx_game_pkg.utils import xListStr

        if not num_lst:
            return ""
        continuous_num_lst, single_lst = cls.merge_continuous_num(
            num_lst, single_split_len=single_split_len, batch_num=batch_num
        )
        p_where_str_list = []
        for data in continuous_num_lst:
            p_where_str_list.append(f"({cls.FILLKEY} between {data[0]} and {data[1]})")
        if single_lst:
            p_where_str_list.append(f"({cls.FILLKEY} in ({xListStr.lst2str(single_lst)}))")
        p_where_str = f"({' OR '.join(p_where_str_list)})"

        if key_name:
            p_where_str = p_where_str.replace(cls.FILLKEY, key_name)
        return p_where_str

    @classmethod
    def merge_continuous_num(cls, num_lst: list[int], single_split_len: int = 5, batch_num: int = 0):
        """
        合并连续的数字
        把[1,2,3,5,6,8] => [[1,3],[5,6],[8,8]]
        :param num_lst: 数据列表
        :param single_split_len: 连续长度[最大值-最小值]>=该值才能被记作连续
        :param batch_num: 分批次处理的长度
        :return: single_split_len>0时,返回 (new_continuous_list, single_list)
            single_split_len==0是,返回 new_continuous_list
        """
        num_lst = list(sorted(set(num_lst)))
        num_len = len(num_lst)
        batch_num = batch_num or num_len
        result = []
        for idx in range(0, num_len, batch_num):
            part_num_lst = num_lst[idx : idx + batch_num]
            if part_num_lst[0] + len(part_num_lst) - 1 == part_num_lst[-1]:
                # 首尾完全符合连续性
                result.append([part_num_lst[0], part_num_lst[-1]])
            else:
                # 合并当前批次的连续数字
                result.extend(cls.do_merge_num(part_num_lst))
        return cls.do_merge_num(result, single_split_len=single_split_len)

    @staticmethod
    def do_merge_num(num_lst, single_split_len=0):
        continuous_list = []
        for idx, data in enumerate(num_lst):
            if isinstance(data, list):
                left, right = data
            else:
                left = right = data
            if continuous_list:
                last_left, last_right = continuous_list[-1]
                if last_right + 1 == left:
                    continuous_list[-1] = [last_left, right]
                    continue
            continuous_list.append([left, right])

        if single_split_len:
            new_continuous_list = []
            single_list = []
            for data in continuous_list:
                if data[-1] - data[0] < single_split_len:
                    single_list.extend(list(range(data[0], data[-1] + 1)))
                else:
                    new_continuous_list.append(data)
            return new_continuous_list, single_list
        return continuous_list
