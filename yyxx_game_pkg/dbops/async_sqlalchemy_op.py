# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2024/11/13
"""

import re
import pandas as pd
from sqlalchemy import text
from yyxx_game_pkg.dbops.base import DatabaseOperation
from yyxx_game_pkg.utils import xListStr
from yyxx_game_pkg.statistic.log import debug_log
from sqlalchemy import MetaData, Table


class AsyncSqlalchemyOperation(DatabaseOperation):
    """
    sqlalchemy数据库通用操作
    """

    # 创建 MetaData 对象
    metadata = MetaData()

    async def get_table(self, conn, table_name, metadata=None):
        """使用反射加载表"""
        return await conn.run_sync(
            lambda async_conn: Table(table_name, metadata or self.metadata, autoload_with=async_conn)
        )

    @staticmethod
    def check_sql(sql, conn=None, params=None):
        """
        检查sql表述是否正确
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        return text(sql)

    async def execute(self, sql, conn, params=None):
        """
        执行sql返回处理结果
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        sql = self.check_sql(sql, conn, params)
        async with conn:
            if params is None:
                await conn.execute(sql)
            else:
                await conn.execute(sql, params)
            await conn.commit()

    async def get_one(self, sql, conn, params=None):
        """
        查询一条数据, 返回元组结构
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        sql = self.check_sql(sql, conn, params)
        async with conn:
            if params is None:
                return (await conn.execute(sql)).fetchone()
            else:
                return (await conn.execute(sql, params)).fetchone()

    async def get_all(self, sql, conn, params=None):
        """
        查询多条数据，返回list(元组) 结构
        :param sql:
        :param conn:
        :param params:
        :return:
        """
        sql = self.check_sql(sql, conn, params)
        async with conn:
            if params is None:
                return (await conn.execute(sql)).fetchall()
            else:
                return (await conn.execute(sql, params)).fetchall()

    async def get_all_df(self, sql, conn):
        """
        获取所有数据 dataframe
        :param sql:
        :param conn:
        :return:
        """
        sql = self.check_sql(sql, conn)
        async with conn:
            result = await conn.execute(sql)
            data = result.fetchall()
            columns = list(result.keys())
            return pd.DataFrame(data, columns=columns)

    @staticmethod
    def tuples_to_dicts(tuples, column_names):
        # 将元组列表转换为字典列表
        return [dict(zip(column_names, t)) for t in tuples]

    @staticmethod
    def replace_percent_sql(sql, arg_format="{}") -> tuple[str, int]:
        """
        使用正则表达式找到所有的 %s, 并依次替换为 ":{arg_format}{counter}"
        :param sql:
        :param arg_format:
        :return:
        """

        def replacer(match):
            nonlocal counter
            counter += 1
            return ":" + arg_format.format(counter)

        counter = 0
        after_sql = re.sub(r"%s", replacer, sql)

        if sql != after_sql:
            debug_log(f"[AsyncSqlalchemyOperation][replace_percent_sql] 前=>{sql}")
            debug_log(f"[AsyncSqlalchemyOperation][replace_percent_sql] 后=>{after_sql}")
        return after_sql, counter

    async def insert(self, conn, save_table="", results=(), insert_sql=""):
        results = xListStr.split_list(results)
        async with conn:
            if insert_sql:
                arg_format = "arg_{}"
                insert_sql, arg_len = self.replace_percent_sql(insert_sql, arg_format)
                tb_columns = [arg_format.format(flag) for flag in range(1, arg_len + 1)]
                statement = text(insert_sql)
            else:
                table = await self.get_table(conn, save_table)
                tb_columns = [column.name for column in table.columns if column.name not in ("id", "create_time")]
                statement = table.insert()
            for result in results:
                if not result:
                    continue
                await conn.execute(statement, self.tuples_to_dicts(result, tb_columns))
            await conn.commit()
