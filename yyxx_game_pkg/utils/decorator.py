# -*- coding: utf-8 -*-
"""
@File: decorator
@Author: ltw
@Time: 2022/8/4
"""
import functools
import pickle
import random
import time
import traceback
from concurrent import futures
import os

from yyxx_game_pkg.logger.log import root_log
from yyxx_game_pkg.xtrace.helper import get_current_trace_id


def fix_str(obj, max_len=5000):
    """
    切割过长str, 避免打印过多无用信息
    """
    msg = str(obj)
    return msg[0 : min(len(msg), max_len)]


def log_execute_time_monitor(exec_lmt_time=20):
    """
    超时函数监控
    :param exec_lmt_time:秒
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def inner(*args, **kwargs):
            begin_dt = time.time()
            res = func(*args, **kwargs)
            end_dt = time.time()
            offset = end_dt - begin_dt
            if offset >= exec_lmt_time:
                ex_info = None
                if kwargs.get("connection") is not None:
                    ex_info = kwargs.get("connection")._con._kwargs.get("host")
                _args = []
                for _arg in args:
                    _args.append(fix_str(_arg, 100))
                for k, _v in kwargs.items():
                    kwargs[k] = fix_str(_v, 100)
                trace_id = get_current_trace_id()
                root_log(
                    f"<log_execute_time_monitor> trace_id: {trace_id} "
                    f"func <<{func.__name__}>> deal over time "
                    f"begin_at: {begin_dt} end_at: {end_dt}, sec: {offset}"
                    f"ex_info{ex_info}, params: {str(args)}, {str(kwargs)}"
                )
            return res

        return inner

    return decorator


def except_monitor(func):
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
            _args = []
            for _arg in args:
                _args.append(fix_str(_arg, 100))
            for k, _v in kwargs.items():
                kwargs[k] = fix_str(_v, 100)
            root_log(
                "<except_monitor>"
                f"func:{func.__module__}.{func.__name__}, args:{str(_args)}, kwargs:{str(kwargs)}, "
                f"exc: {traceback.format_exc()} {e}",
                level="error",
            )
        return res

    return inner


def except_return(default=None, echo_raise=True):
    """
    # 异常后指定返回值
    :param default: 返回值(或者可执行函数)
    :param echo_raise: 是否打印报错信息
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if echo_raise:
                    _args = []
                    for _arg in args:
                        _args.append(fix_str(_arg, 100))
                    for k, _v in kwargs.items():
                        kwargs[k] = fix_str(_v, 100)
                    root_log(
                        "<except_return>"
                        f"func:{func.__module__}.{func.__name__}, args:{str(_args)}, kwargs:{str(kwargs)}, "
                        f"exc: {traceback.format_exc()} {e}",
                        level="error",
                    )

                return default(e=e, f_args=args, f_kwargs=kwargs) if callable(default) else default

        return wrapper

    return decorator


def singleton(cls):
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance


def singleton_unique(cls):
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kw):
        unique_key = f"{os.getpid()}_{cls}_{args}_{kw}"
        if unique_key not in instances:
            instances[unique_key] = cls(*args, **kw)
        return instances[unique_key]

    return get_instance


def singleton_unique_obj_args(cls):
    # object 需重写 __str__
    instances = {}

    @functools.wraps(cls)
    def get_instance(*args, **kw):
        unique_key = f"{os.getpid()}_{cls}_{list(map(str, args))}_{kw}"
        if unique_key not in instances:
            instances[unique_key] = cls(*args, **kw)
        return instances[unique_key]

    return get_instance


def timeout_run(timeout=2, default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                executor = futures.ThreadPoolExecutor(1)
                future = executor.submit(func, *args, **kw)
                return future.result(timeout=timeout)
            except Exception as e:
                root_log(f"timeout_run {func} error {e} args:{args} kw:{kw}")
                return default

        return wrapper

    return decorator


# 缓存装饰器[仅支持可序列化返回值]
# todo 重启服务清空缓存
def redis_cache_result(handle, redis_key=None, prefix="_fix", sec=3600):
    """
    :param handle: redis连接
    :param redis_key: 需保持唯一性 默认为函数名
    :param prefix: key前缀 避免冲突
    :param sec: 过期时间(秒) + 随机0 ~ 30
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                _arg = pickle.dumps(args)
            except Exception:
                # 静默处理
                _arg = pickle.dumps(args[1:])
            _kwargs = pickle.dumps(kwargs)
            # 不指明redis_key默认用func.name
            cache_key = redis_key if redis_key else func.__name__
            # prefix 防止与其他模块的缓存key冲突
            cache_key = f"{prefix}_{cache_key}_{_arg}_{_kwargs}"
            cache_data = handle.get_data(cache_key)
            if cache_data:
                res = pickle.loads(cache_data)
                return res
            res = func(*args, **kwargs)
            handle.set_data(
                cache_key, pickle.dumps(res), ex=sec + random.randint(0, 30)
            )
            return res

        return wrapper

    return decorator
