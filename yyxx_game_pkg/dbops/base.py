# -*- coding: utf-8 -*-
"""
@File: base.py
@Author: ltw
@Time: 2023/4/4
"""
import pandas as pd


class DatabaseOperation:
    """
    db 操作基类
    """

    def __init__(self):
        pass

    @staticmethod
    def check_sql(sql):
        """
        检查sql表述是否正确
        :param sql:
        :return:
        """
        # TODO ltw
        return sql

    def execute(self, *args, **kwargs):
        """
        执行sql表述
        :param args:
        :param kwargs:
        :return:
        """

    def insert(self, *args, **kwargs):
        """
        插入数据
        :param args:
        :param kwargs:
        :return:
        """

    def get_one(self, *args, **kwargs):
        """
        获取单次数据
        :param args:
        :param kwargs:
        :return:
        """

    def get_all(self, *args, **kwargs):
        """
        获取所有数据
        :param args:
        :param kwargs:
        :return:
        """

    def get_one_df(self, *args, **kwargs) -> pd.DataFrame:
        """
        获取单次数据
        :param args:
        :param kwargs:
        :return:
        """

    def get_all_df(self, *args, **kwargs) -> pd.DataFrame:
        """
        获取所有数据 dataframe
        :param args:
        :param kwargs:
        :return:
        """
