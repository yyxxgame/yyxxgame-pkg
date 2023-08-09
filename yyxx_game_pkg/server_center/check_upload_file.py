# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/06/26 11:26:33
# @Software : python3.11
# @Desc     : 解析上传文件（Django）
"""
使用方式
需要继承 CheckUploadFile，实现 process（检测和获取每行数据）
其他说明：prepare方法，对数据做预处理
        kwargs参数: 需要额外添加的数据，可以放在里面
"""
import os
from typing import Iterable

import numpy as np
import pandas as pd
from django.core.files.uploadedfile import InMemoryUploadedFile
from yyxx_game_pkg.helpers.op_helper import OPHelper
from yyxx_game_pkg.utils.files import get_file_size


class CheckUploadFile(OPHelper):
    def __init__(
        self,
        *,
        input_file_name="upload_file",
        file_max_size="10MB",
        file_allow_ext=(".xls", ".xlsx"),
        min_column=0,
        **kwargs,
    ):
        self.total_num = 0
        self.insert_data = []
        self.df = None
        self.input_file_name = input_file_name
        self.file_max_size = file_max_size
        self.file_allow_ext = file_allow_ext
        self.min_column = min_column
        self.kwargs = kwargs
        self.conn = self.connection()

    def check(self, request):
        """Check upload File"""
        input_file_name = self.input_file_name
        if input_file_name not in request.FILES:
            return "请选择文件"

        f: InMemoryUploadedFile = request.FILES[input_file_name]
        file_size = f.size
        file_name = f.name

        if file_size > get_file_size(self.file_max_size):
            return "文件大小不大于{}".format(self.file_max_size)

        file_ext = os.path.splitext(file_name)[1].lower()
        if file_ext not in self.file_allow_ext:
            return "文件格式只支持{}".format(",".join(self.file_allow_ext))

        with f.file as file_io:
            self.df = pd.read_excel(file_io)
        if self.df.empty:
            return "没有符合的记录"

        if len(self.df.iloc[0].tolist()) < self.min_column:
            return "列数至少包含{}行".format(self.min_column)

        self.prepare()

        for i, row in self.df.iterrows():
            row_data = row.tolist()
            serial = row_data[0]
            if np.isnan(serial):
                return "上传的数据，不可以有空行（数据不完整），上传失败"

            msg = self.process(row_data)
            if msg:
                return msg

        if self.total_num == 0:
            return "提交记录至少包含一条"
        if self.total_num > 1000:
            return "单词最多只能提交1000条记录"

        return ""

    def prepare(self):
        """数据预处理"""
        pass

    def process(self, row_data):
        """处理每行的数据
        :param row_data: 行数据
        """
        self.insert_data.append(row_data)
        self.total_num += 1
        return ""

    @staticmethod
    def insert_sql(
        table: str, fields: Iterable, update=False, update_fields: Iterable = ()
    ) -> str:
        """合成sql语句
        :param table: 要插入的表名
        :param fields: 要插入的字段
        :param update: 是否需要 ON DUPLICATE KEY UPDATE
        :param update_fields: 需要更新的字段，如果没有，则使用fields
        """
        sql = f"INSERT INTO {table} ({','.join(fields)}) VALUES({','.join(['%s'] * len(fields))})"
        if update:
            update_list = []
            _fields = update_fields if update_fields else fields
            for field in _fields:
                update_list.append(f"{field}=VALUES({field})")
            sql += f" ON DUPLICATE KEY UPDATE {','.join(update_list)}"
        return sql

    def insert(
        self,
        sql: str = None,
        table: str = None,
        fields: tuple | list = None,
        update=False,
        update_fields=(),
    ):
        """把数据插入表处理
        :param sql: 完整的sql语句
        :param table: 要插入的表名
        :param fields: 要插入的字段
        :param update: 是否需要 ON DUPLICATE KEY UPDATE
        :param update_fields: 需要更新的字段，如果没有，则使用fields
        """
        code = -1001
        if table and fields:
            sql = self.insert_sql(table, fields, update, update_fields)

        if sql is None:
            msg = "请填写sql"
            return code, msg

        with self.conn.cursor() as cursor:
            for item in self.insert_data:
                try:
                    cursor.execute(sql, item)
                except Exception as e:
                    msg = str(e)
                    self.conn.rollback()
                    return code, msg

        self.conn.commit()
        return 1, ""

    def __del__(self):
        self.conn.close()
