# -*- coding: utf-8 -*-
"""
@File: xListStr.py
@Author: ltw
@Time: 2023/3/31
"""
import ujson as json


def lst2str(lst, isdigit=True, symbol=",", warp="'") -> str:
    """
    list转字符串
    lst2str(['a', 'b', 'c]) -> "'a', 'b', 'c'"
    :param lst:
    :param isdigit:
    :param symbol:
    :param warp: 字符串包裹符 默认单引号
    :return:
    """
    if not lst:
        return ""
    if isinstance(lst, int):
        lst = [lst]

    if not isinstance(lst, list):
        lst = list(lst)

    # 简单情况自动处理
    if not str(lst[0]).isdigit():
        isdigit = False

    def _str(_s):
        return f"{warp}{_s}{warp}"

    lst = list(map(str, lst)) if isdigit else list(map(_str, lst))
    lst_str = symbol.join(lst)
    return lst_str


def load_js_str_keys(js_str, keys, default=None) -> dict:
    """
    load json字符串中指定key列表
    :param js_str:
    :param keys:
    :param default:
    :return: dict
    """
    # 返回键值对
    if default is None:
        default = {}
    if not js_str:
        return {}
    js_dict = json.loads(js_str)
    res = {}
    for key in keys:
        res[key] = js_dict.get(key, default)
    return res


def str2list(list_str, split_symbol) -> list:
    """
    str转list 去除空项
    str2list("#1#2##", "#") -> ['1', '2']
    :param list_str:
    :param split_symbol:
    :return:
    """

    def filter_func(val):
        if not val:
            return False
        return True

    res = list(filter(filter_func, list_str.split(split_symbol)))
    return res


def split_list(pending_lst, split_size=50000) -> list:
    """
    列表切分
    split_list([[1, 2, 3, 4, 5]], 3) -> [[1, 2, 3], [4, 5]]
    split_list([1, 2, 3, 4, 5], 3) -> [[1, 2, 3], [4, 5]]
    :param pending_lst:
    :param split_size:
    :return:
    """
    if not isinstance(pending_lst, (list, tuple)):
        return pending_lst
    if len(pending_lst) != 1:
        pending_lst = [pending_lst]
    base_num = split_size
    result = pending_lst[0]
    size = len(result) / base_num
    if len(result) % base_num != 0:
        size += 1
    data_list = []
    for index in range(int(size)):
        data_list.append(result[index * base_num : (index + 1) * base_num])
    return data_list


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