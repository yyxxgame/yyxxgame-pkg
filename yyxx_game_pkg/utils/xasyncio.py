# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2025/2/19
"""
import asyncio
import datetime
from yyxx_game_pkg.statistic.log import debug_log


class EmptyAsyncSemaphore:
    async def __aenter__(self):
        pass

    async def __aexit__(self, exc_type, exc, tb):
        pass


class AsyncTask:
    def __init__(self, async_func, *args, semaphore: asyncio.Semaphore = None, **kwargs):
        self.async_func = async_func
        self.semaphore = semaphore or EmptyAsyncSemaphore()

    async def call(self):
        async with self.semaphore:
            debug_log(
                f"[AsyncTask] [{datetime.datetime.now()}][{id(self.async_func)}]{self.async_func.__name__} 开始跑啦"
            )
            data = await self.async_func
            debug_log(
                f"[AsyncTask] [{datetime.datetime.now()}][{id(self.async_func)}]{self.async_func.__name__} 跑完啦"
            )
            return data


def async_run(*aws, to_list=False, poll_size=0):
    """
    :param aws:
    :param to_list: 为True时,即使只有1个任务, 也返回list
    :param poll_size: 协程并发度
    :return:
    """
    async_semaphore = asyncio.Semaphore(poll_size) if poll_size > 0 else EmptyAsyncSemaphore()

    async def async_gather(*args):
        """
        :param args:
        :return:
        """
        return await asyncio.gather(*[AsyncTask(async_func=arg, semaphore=async_semaphore).call() for arg in args])

    if len(aws) > 1 or to_list:
        results = asyncio.run(async_gather(*aws))
    else:
        results = asyncio.run(*aws)
    return results
