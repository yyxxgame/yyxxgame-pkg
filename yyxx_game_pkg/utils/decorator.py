# -*- coding: utf-8 -*-
"""
@File: decorator
@Author: ltw
@Time: 2022/8/4
"""
import time
import functools
from yyxx_game_pkg.logger.log import local_log


def trans_str(obj, max_len=5000):
    msg = str(obj)
    return msg[0: min(len(msg), max_len)]


def log_execute_time_monitor(exec_lmt_time=20):
    """
    超时函数监控
    :param exec_lmt_time:秒
    :return:
    """

    def decorator(func):
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
                    _args.append(trans_str(_arg, 100))
                for k, v in kwargs.items():
                    kwargs[k] = trans_str(v, 100)
                local_log(
                    f"<log_execute_time_monitor>func <<{func.__name__}>> deal over time "
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
            import traceback

            _args = []
            for _arg in args:
                _args.append(trans_str(_arg, 100))
            for k, v in kwargs.items():
                kwargs[k] = trans_str(v, 100)
            local_log(
                f"<except_monitor> "
                f"func:{func.__module__}.{func.__name__}, args:{str(_args)}, kwargs:{str(kwargs)}, "
                f"exc: {traceback.format_exc()} {e}"
            )
        return res

    return inner


def except_return(default=None):
    """
    # 异常后指定返回值
    :param default: 返回值
    :return:
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                return func(*args, **kw)
            except Exception as e:
                import traceback

                print("{}: exc:{}".format(e, traceback.format_exc()))
                return default

        return wrapper

    return decorator


def singleton(cls):
    from functools import wraps

    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return get_instance


def singleton_unique(cls):
    from functools import wraps

    instances = {}

    @wraps(cls)
    def get_instance(*args, **kw):
        unique_key = "{}_{}_{}".format(cls, args, kw)
        if unique_key not in instances:
            instances[unique_key] = cls(*args, **kw)
        return instances[unique_key]

    return get_instance


def timeout_run(timeout=2, default=None):
    import functools
    from concurrent import futures

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            try:
                executor = futures.ThreadPoolExecutor(1)
                future = executor.submit(func, *args, **kw)
                return future.result(timeout=timeout)
            except Exception as e:
                local_log("timeout_run {} error {} args:{} kw:{}".format(func, e, args, kw))
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
    import random
    import pickle
    import functools

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                _arg = pickle.dumps(args)
            except Exception as e:
                local_log(e)
                _arg = pickle.dumps(args[1:])
            _kwargs = pickle.dumps(kwargs)
            # 不指明redis_key默认用func.name
            _cache_key = redis_key if redis_key else func.__name__
            # prefix 防止与其他模块的缓存key冲突
            _cache_key = "{}_{}_{}_{}".format(prefix, _cache_key, _arg, _kwargs)
            _cache_data = handle.get_data(_cache_key)
            if _cache_data:
                res = pickle.loads(_cache_data)
                return res
            res = func(*args, **kwargs)
            handle.set_data(
                _cache_key, pickle.dumps(res), ex=sec + random.randint(0, 30)
            )
            return res

        return wrapper

    return decorator
