# -*- coding: utf-8 -*-
"""
@File: hdfs_op.py
@Author: ltw
@Time: 2022/7/21
"""
import pandas as pd
from os import path as op
from yyxx_game_pkg.dbops.base import DatabaseOperation


class HdfsOperation(DatabaseOperation):
    """
    hdf5
    """

    def __init__(self, data_path="/opt/hdf5_data/"):
        super().__init__()
        self.data_path = data_path

    def get_one_df(self, *args, **kwargs) -> pd.DataFrame:
        """
        :param args:
        :param kwargs:
        :return:
        """

    def get_all_df(self, data_dir, data_keys, columns=None, where=None):
        """
        :param data_dir:
        :param data_keys:
        :param columns:
        :param where:
        :return:
        """
        the_path = op.join(self.data_path, data_dir)
        res_df = None
        if not isinstance(data_keys, list):
            data_keys = [data_keys]
        for data_key in data_keys:
            data_path = op.join(the_path, f"{data_key}.h5")
            if not op.exists(data_path):
                continue
            hdf_store = pd.HDFStore(data_path, mode="r")
            if columns and where:
                tmp_df = hdf_store.select(data_key, columns=columns, where=where)
            elif columns:
                tmp_df = hdf_store.select(data_key, columns=columns)
            elif where:
                tmp_df = hdf_store.select(data_key, where=where)
            else:
                tmp_df = hdf_store.select(data_key)

            if res_df is None:
                res_df = tmp_df
            else:
                res_df = res_df.append(tmp_df)
        if res_df is None:
            res_df = pd.DataFrame()
        return res_df
