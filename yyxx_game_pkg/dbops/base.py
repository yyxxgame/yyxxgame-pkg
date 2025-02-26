# -*- coding: utf-8 -*-
"""
@File: base.py
@Author: ltw
@Time: 2023/4/4
"""
import re
import typing
import datetime
import pandas as pd
from yyxx_game_pkg.utils import xasyncio, xListStr, xdate


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


class DatabaseOperationProxy:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def split_sql(sql, split_lst, size) -> list:
        """
        :param sql: sql 字符串 如:"select * from table where player_id in ({{split_lst}})"
        :param split_lst: format sql字符串模版 参数value列表
        :param size: 参数列表切分大小
        :return: sql列表 list([sql1, sql2, ...])
        """
        in_lst = xListStr.split_list([split_lst], size)
        sql_lst = []
        sql_fmt = sql.replace("{{", "{").replace("}}", "}")
        for _in in in_lst:
            sql_lst.append(sql_fmt.format(split_lst=xListStr.lst2str(_in)))
        return sql_lst

    @staticmethod
    def split_dt_sql(sql, sdate, edate, size=1) -> list:
        """
        :return: sql列表 list([sql1, sql2, ...])
        :param sql:  sql 字符串 如:"select * from table where log_dt Between '{{sdate}}' AND '{{edate}}'"
        :param sdate: 日期字符串 如 2024-01-01/2024-01-01 04:00:00 (只会取日期部分)
        :param edate: 日期字符串 如 2024-01-01/2024-01-01 04:00:00 (只会取日期部分)
        :param size: 日期切分大小 (默认按天)
        :return: sql列表
        """
        split_lst = list(
            pd.date_range(start=pd.to_datetime(str(sdate)).date(), end=pd.to_datetime(str(edate)).date(), freq="D")
        )
        sql_lst = []
        sql_fmt = re.sub(r"(!\{+)(sdate|edate|sdate4|edate4)(!}+)", r"{\1}", sql)
        for lst in xListStr.split_list([split_lst], size):
            sdate = lst[0]
            edate = lst[-1] + datetime.timedelta(days=1, seconds=-1)
            sql_lst.append(
                sql_fmt.format(
                    sday=xdate.date2day(sdate),
                    eday=xdate.date2day(edate),
                    sdate=sdate,
                    edate=edate,
                    sdate4=sdate + datetime.timedelta(hours=4),
                    edate4=edate + datetime.timedelta(hours=4),
                )
            )
        return sql_lst

    def get_split_sql_df(
        self,
        sql: str,
        db_query_func,
        size=0,
        split_lst: list = (),
        map_lst: list = (),
        sdate: typing.Union[str, datetime.datetime] = "",
        edate: typing.Union[str, datetime.datetime] = "",
        is_async: bool = False,
        async_poll_size=0,
        *args,
        **kwargs,
    ):
        """
        数据切分查询
        :param sql:
            使用split_lst时, 请包含{split_lst}或{{split_lst}}
            使用sdate,edate时 请包含 {sdate} {edate} {sdate4} {edate4} (其中使用{或{{都可)
        :param db_query_func: db查询的函数, 函数本身需以dataframe作为返回类型
        :param size: 每批次的数据长度
            使用split_lst时, 默认为5000, 为list长度
            使用sdate,edate时, 默认为1, 为日期长度(天)
        :param split_lst: 数据lst, 用于按长度切分数据集, 比如批量区服,玩家等, 再进行查询
        :param map_lst: 数据lst, 可以是[{},{}], [(),()], [data1,data2] 不会做二次切分,每个元素都会生成一条sql
        :param sdate: 起始日期 (不管是否带时间, 都只会取日期部分)
        :param edate: 结束日期 (不管是否带时间, 都只会取日期部分)
        :param args: 传入db_query_func的参数
        :param kwargs: 传入db_query_func的参数
        :param is_async: 是否为异步查询, 将调用async_run执行
        :param async_poll_size: async_run.poll_size参数
        :return: db_query_func执行结果

        例子:
        1:按角色/区服切分查询(5000)
        sql= '''
            SELECT player_id, server_id, player_name, is_inner
            FROM [ch_db].log_player_op_v_info_new
            WHERE player_id IN ({{split_lst}})
        '''
        self.get_split_sql_df(sql, split_lst=player_df["player_id"].tolist(), db_query_func=self.get_ch_df, size=5000)
        2:按日期切分查询, 且使用异步并发查询
        sql = f'''
            SELECT day, COUNT(DISTINCT player_id) AS pcnt,
            FROM stat_common_player[_suffix]
            WHERE log_dt BETWEEN '{{sdate}}' AND '{{edate}}' AND event='stat_player_slice_4'
            GROUP BY day
        '''
        res_df = self.get_split_sql_df(
            sql,
            db_query_func=self.async_get_es_df,
            sdate=params_obj.sdate,
            edate=params_obj.edate,
            is_async=True,
            async_poll_size=5,
        ).fillna(0)
        3:map查询, 及遍历查询
        sql = f'''
            SELECT day, count(prop.shape."{{shape_type}}".fashion."{{fashion_id}}") cnt
            FROM stat_common_player[_suffix]
            WHERE log_dt BETWEEN '{params_obj.sdate}' AND '{params_obj.edate}' AND event='stat_player_slice_4'
            GROUP BY day
        '''
        res_df = self.get_split_sql_df(
            sql,
            db_query_func=self.get_es_df,
            map_lst=[
                {'shape_type':12, 'fashion_id':121001},
                {'shape_type':12, 'fashion_id':121002},
                {'shape_type':1, 'fashion_id':11001}
            ]
        ).fillna(0)
        """
        if split_lst:
            size = size or 5000
            split_lst = list(map(int, split_lst))
            sql_lst = self.split_sql(sql, split_lst, size)
        elif map_lst:
            sql_lst = []
            sql_fmt = sql.replace("{{", "{").replace("}}", "}")
            for params in map_lst:
                if isinstance(params, dict):
                    sql_lst.append(sql_fmt.format(**params))
                elif isinstance(params, (list, tuple)):
                    sql_lst.append(sql_fmt.format(*params))
                else:
                    sql_lst.append(sql_fmt.format(params))
        elif sdate and edate:
            size = size or 1
            sql_lst = self.split_dt_sql(sql, sdate, edate, size)
        else:
            return db_query_func(sql, *args, **kwargs)
        res_df_lst = []
        for _sql in sql_lst:
            res_df = db_query_func(_sql, *args, **kwargs)
            res_df_lst.append(res_df)
        if is_async:
            res_df_lst = xasyncio.async_run(*res_df_lst, to_list=True, poll_size=async_poll_size)
        return pd.concat(res_df_lst, ignore_index=True)
