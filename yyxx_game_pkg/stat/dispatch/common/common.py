# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14
import functools

from fastapi.exceptions import HTTPException

from yyxx_game_pkg.stat.dispatch.common.log import local_log
from yyxx_game_pkg.xtrace.helper import get_current_trace_id, add_span_events


def split_list(target_list, list_per_len):
    """
    把target_list分割成若干个小list（连续切割）
    :param target_list: [1,2,3]
    :param list_per_len: 分割块大小:1
    :return: [[1],[2],[3]]
    """
    if not isinstance(target_list, list):
        return []

    if list_per_len <= 0:
        return [[]]

    f_split = lambda a, l: map(lambda b: a[b : b + l], range(0, len(a), l))
    return f_split(target_list, list_per_len)


def get_queue_name(queue_name):
    if queue_name is None:
        return None
    return queue_name.split("@")[0]


def fastapi_except_monitor(func):
    """
    异常处理捕捉装饰器
    打印全部参数
    :return:
    """

    @functools.wraps(func)
    def inner(*args, **kwargs):
        res = None
        try:
            res = func(*args, **kwargs)
        except Exception as e:
            import traceback

            err_log = f"<except_monitor> func:{func.__module__}.{func.__name__} exc: {traceback.format_exc()} {e}"
            local_log(err_log)
            err_msg = {"detail": err_log, "trace_id": get_current_trace_id()}
            add_span_events("error", err_msg)
            raise HTTPException(status_code=500, detail=err_msg)
        return res

    return inner
