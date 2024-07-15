# -*- coding: utf-8 -*-
"""
@File: base.py
@Author: ltw
@Time: 2023/6/14
"""
import pandas as pd

from .async_das_client import AsyncDasClient


class AsyncDatabaseOperation:
    """
    db 操作基类
    """

    def __init__(self, das_url):
        self.das_url = das_url
        self.async_das_client = AsyncDasClient()

    async def execute(self, *args, **kwargs):
        """
        执行sql表述
        :param args:
        :param kwargs:
        :return:
        """

    async def insert(self, *args, **kwargs):
        """
        插入数据
        :param args:
        :param kwargs:
        :return:
        """

    async def get_one(self, *args, **kwargs):
        """
        获取单次数据
        :param args:
        :param kwargs:
        :return:
        """

    async def get_all(self, *args, **kwargs):
        """
        获取所有数据
        :param args:
        :param kwargs:
        :return:
        """

    async def get_one_df(self, *args, **kwargs) -> pd.DataFrame:
        """
        获取单次数据
        :param args:
        :param kwargs:
        :return:
        """

    async def get_all_df(self, *args, **kwargs) -> pd.DataFrame:
        """
        获取所有数据 dataframe
        :param args:
        :param kwargs:
        :return:
        """
