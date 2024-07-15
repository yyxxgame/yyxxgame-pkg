# -*- coding: utf-8 -*-
"""
@File: data_types
@Author: ltw
@Time: 2024/7/15
"""

import numpy as np


def trans_unsupported_types(val):
    """
    转化json.dumps不支持的数据类型 : int64, bytes, ...
    :param val:
    :return:
    """
    if isinstance(val, dict):
        new_dict = {}
        for k, _v in val.items():
            k = trans_unsupported_types(k)
            _v = trans_unsupported_types(_v)
            new_dict[k] = _v
        return new_dict
    if isinstance(val, list):
        for idx, _v in enumerate(val):
            _v = trans_unsupported_types(_v)
            val[idx] = _v
    elif isinstance(val, np.int64):
        val = int(val)
    elif isinstance(val, bytes):
        val = val.decode(encoding="utf8")
    return val
