# -*- coding: utf-8 -*-
"""
@File: xdataframe
@Author: ltw
@Time: 2022/8/4
"""
import json
from bisect import bisect_left
import pandas as pd
import numpy as np


def empty_df(columns=None):
    """
    :param columns:
    :return:
    """
    if not columns:
        return pd.DataFrame()
    return pd.DataFrame(columns=columns)


def df_col2row_idx(_df, index_keys, data_key):
    """
    # df 列转行索引
    #
    #           day      player_id   money
    # 0    20210527  1508277000053     6.0
    # 1    20210527  1508277000058     6.0
    # 3    20210528  1508277000058     12.0
    #
    # res_df = df_col2row_idx(res_df, ['player_id', 'day'], 'money')
    #
    #         player_id  20210527  20210528
    # 0    1508277000053       6.0       NaN
    # 1    1508277000058       6.0       12.0
    """
    df_index = _df.set_index(index_keys)[data_key]
    _df = df_index.unstack()
    _df = _df.rename_axis(None, axis="columns").reset_index()
    return _df


def cut_bins(val, bins, concat="-"):
    """
    :param val:
    :param bins:
    :param concat:
    :return:
    """
    if not val:
        return val

    if val > bins[-1]:
        val = bins[-1]

    position = bisect_left(bins, val)
    labels = f"{bins[position - 1] + 1}{concat}{ bins[position]}"
    return labels, bins[position]


def df_cut_bins(_df, key, bins, insert_zero=True):
    """
    :param _df:
    :param key:
    :param bins:
    :param insert_zero:
    :return:
    """

    def prefix_bins(_bins):
        """
        排序
        :param _bins:
        :return:
        """
        _bins = sorted(map(int, _bins))
        if insert_zero and _bins[0] != 0:
            _bins.insert(0, 0)
        return _bins

    bins = prefix_bins(bins)
    return _df[key].apply(cut_bins, bins=bins)


def cal_round_rate(data, precision=2, suffix="%"):
    """
    :param data:
    :param precision:
    :param suffix:
    :return:
    """
    if isinstance(data, pd.DataFrame):
        return data.apply(cal_round_rate, args=(precision, suffix), axis=0)
    if isinstance(data, pd.Series):
        return data.round(precision).apply(
            lambda d: "-" if (d == np.inf or np.isnan(d)) else f"{d}{suffix}"
        )
    if isinstance(data, (int, float)):
        return str(round(data, 2)) + suffix
    return "-"


def func_cal_round_rate(func, **kw):
    """
    用于快速构造用agg或apply传递的cal_round_rate函数
    :param func:
    :param kw:
    :return:
    """

    def wrapper(data, *args, **kwargs):
        if isinstance(func, str):
            data = getattr(data, func)()
        else:
            data = func(data)
        return cal_round_rate(data, **kw)

    return wrapper


def dict_to_json(data):
    """用于es对象转json,并且正常显示中文"""
    if not data:
        return data
    if isinstance(data, float) and pd.isna(data):
        return ""
    return json.dumps(data, ensure_ascii=False)


def df_json_normalize(_df, columns, prefixes=None, sep=".", column_prefix=False):
    """
    df: 原df数据
    record_paths: 需要解析的列名list
    record_prefixes: 需要填充前缀list
    sep: 填充前缀的分隔符
    column_prefix: 使用字段名作为前缀
    """
    for idx, record_column in enumerate(columns):
        tmp_df = pd.DataFrame(_df[record_column].tolist())
        record_prefix = None
        if column_prefix:
            record_prefix = record_column
        elif prefixes is not None:
            record_prefix = prefixes[idx]
        if record_prefix:
            tmp_df.columns = [f"{record_prefix}{sep}{col}" for col in tmp_df.columns]
        _df[tmp_df.columns] = tmp_df
        _df = _df.drop(columns=record_column)
    return _df


def df_fill_columns(_df, columns, default="", tpe=None):
    """
    填充列,以确保列存在
    """
    if isinstance(columns, (list, tuple)):
        for column in columns:
            if column not in _df.columns:
                _df[column] = default
            elif tpe:
                _df[column] = _df[column].fillna(default).astype(tpe)
            else:
                _df[column] = _df[column].fillna(default)

    elif isinstance(columns, dict):
        for column, val in columns.items():
            if column not in _df.columns:
                _df[column] = val
            elif tpe:
                _df[column] = _df[column].fillna(default).astype(tpe)
            else:
                _df[column] = _df[column].fillna(default)
    else:
        if columns not in _df.columns:
            _df[columns] = default
        elif tpe:
            _df[columns] = _df[columns].fillna(default).astype(tpe)
        else:
            _df[columns] = _df[columns].fillna(default)
    return _df


def df_rm_columns(_df, columns):
    """
    安全删除列
    :param _df:dataframe or series
    :param columns:需删除的列或index
    :return:新的dataframe or series
    """
    if isinstance(_df, pd.Series):
        rm_columns = [column for column in columns if column in _df.index]
        if rm_columns:
            _df = _df.drop(rm_columns)
    else:
        rm_columns = [column for column in columns if column in _df.columns]
        if rm_columns:
            _df = _df.drop(columns=rm_columns)
    return _df
