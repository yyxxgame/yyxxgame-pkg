# -*- coding: utf-8 -*-
"""
@File: xfutures.py
@Author: ltw
@Time: 2023/6/12
"""

from concurrent.futures import ThreadPoolExecutor
from typing import Callable

from opentelemetry import context as trace_context


class FunctorWithTrace:
    """
    用于处理多线程执行任务时trace上下文丢失
    ThreadPoolExecutor submit时使用该类包裹，自动添加trace上下文
    with ThreadPoolExecutor(max_workers=50) as executor:
        executor.submit(FunctorWithTrace(funcxxx, *args, **kwargs))
    """

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = []
        for _arg in args:
            self._args.append(_arg)

        self.group = kwargs.pop("group", None)
        self.context = trace_context.get_current()
        self._kwargs = kwargs

    def __call__(self, *args, **kwargs):
        trace_context.attach(self.context)
        self._args.extend(args)
        self._kwargs.update(kwargs)
        return self._func(*self._args, **self._kwargs)

    def __del__(self):
        self._func = None
        self._args = None
        self._kwargs = None


class TracedThreadPoolExecutor(ThreadPoolExecutor):
    """
    用于处理多线程执行任务时trace上下文丢失，自动添加上下文
    with TracedThreadPoolExecutor(max_workers=50) as trace_executor:
        trace_executor.submit(funcxxx, *args, **kwargs)
    """

    @staticmethod
    def with_trace_context(context: trace_context.Context, func: Callable):
        """
        :param context:
        :param func:
        :return:
        """
        trace_context.attach(context)
        return func()

    def submit(self, fn, *args, **kwargs):
        """
        :param fn:
        :param args:
        :param kwargs:
        :return:
        """

        # get the current trace context
        context = trace_context.get_current()
        if context:
            return super().submit(
                lambda: self.with_trace_context(context, lambda: fn(*args, **kwargs)),
            )
        return super().submit(lambda: fn(*args, **kwargs))
