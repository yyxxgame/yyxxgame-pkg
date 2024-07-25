# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2024/2/26
"""

import os
import copy
import math
import typing
import logging
import datetime
import pandas as pd


class XlsxOperate:
    """
    Excel操作
    """

    @staticmethod
    def save_xlsx(data_df: pd.DataFrame, file_path: str = "", excel_writer: pd.ExcelWriter = None, **kwargs):
        """
        将DataFrame输出到excel_writer。
        :param data_df: 要保存的DataFrame
        :param file_path: 保存文件的路径
        :param excel_writer: Excel写入器
        :param kwargs: to_excel的额外参数
        :return: None
        """
        config = {
            "sheet_name": "Sheet1",
            "index": False,
            "engine": "xlsxwriter",
            "startrow": 0,
        }
        config.update(kwargs)
        if not excel_writer:
            with pd.ExcelWriter(file_path, engine="xlsxwriter") as writer:
                data_df.to_excel(writer, **config)
        else:
            data_df.to_excel(excel_writer, **config)

    @staticmethod
    def get_project_dir():
        """
        获取项目目录(工作目录)
        """

        return os.getcwd()

    @classmethod
    def get_logs_path(cls, file_name=""):
        """
        默认输出到(工作目录/logs)目录下
        :param file_name: 文件名
        :return: 文件路径
        """
        return f"{cls.get_project_dir()}/logs" + (f"/{file_name}" if file_name else "")

    @classmethod
    def get_default_xlsx_path(cls, file_name=""):
        file_name = file_name or datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        return cls.get_logs_path(file_name=f"{file_name}.xlsx")

    @classmethod
    def batch_save_xlsl(
        cls,
        data: typing.Union[pd.DataFrame, dict[str, pd.DataFrame]],
        file_name: str = "",
        batch_count: int = 30000,
        file_path: str = "",
        sheet_max_idx: int = 1000000,
    ):
        """
        批量保存数据到Excel文件中
        :param data: 要保存的数据，可以是DataFrame或字典，字典的键为工作表名称，值为DataFrame
        :param file_name: 保存的Excel文件名(当file_path为空时生效),无需加.xlsx后缀
        :param batch_count: 每次写入的行数，默认为30000
        :param file_path: 保存的Excel文件路径
        :param sheet_max_idx: 每个sheet最大行数, 超过会写入到新的sheet
        :return: None
        注: 优先使用file_path路径, 为空时, 以file_name(为空时,使用时间字符串)作为文件命名并输出到默认Log目录下
        """
        if not isinstance(data, dict):
            data = {"Sheet1": data}
        file_path = file_path or cls.get_default_xlsx_path(file_name)

        # 单sheet超过100w(sheet_max_idx)行, 将数据拆分为多个sheet
        for sheet_name in copy.deepcopy(list(data.keys())):
            data_df = data[sheet_name]
            for split_idx in range(math.ceil(len(data_df) / sheet_max_idx)):
                split_data_df = data_df.iloc[split_idx * sheet_max_idx : (split_idx + 1) * sheet_max_idx]
                if not split_idx:
                    data[sheet_name] = split_data_df
                else:
                    data[f"{sheet_name}_{split_idx+1}"] = split_data_df

        with pd.ExcelWriter(file_path) as writer:
            for sheet_name in data.keys():
                data_df = data[sheet_name]
                _len = len(data_df)
                num_chunks = math.ceil(_len / batch_count)  # 计算总批数
                for i in range(num_chunks):
                    start = i * batch_count
                    end = (i + 1) * batch_count
                    logging.info(
                        f"[XlsxOperate-batch_save_xlsl] 开始写入sheet[{sheet_name}], 第[{start + 1}-{min(end, _len)}]行"
                    )
                    df_chunk = data_df.iloc[start:end]
                    if i == 0:
                        cls.save_xlsx(df_chunk, sheet_name=sheet_name, excel_writer=writer)
                    else:
                        cls.save_xlsx(
                            df_chunk, sheet_name=sheet_name, excel_writer=writer, header=False, startrow=start + 1
                        )
        logging.info(f"[XlsxOperate-batch_save_xlsl] 已导出至 {file_path}")

    @classmethod
    def read_csv_from_logs(cls, file_name, *args, **kwargs):
        data_df = pd.read_csv(cls.get_logs_path(file_name=file_name), *args, **kwargs)
        return data_df
