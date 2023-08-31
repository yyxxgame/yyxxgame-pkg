# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/04/23 09:57:04
# @Software : python3.11
# @Desc     : 操作数据库的类, 继承使用（mysql, redis）
import datetime
import json

from pymysql import Connection
from pymysql.cursors import Cursor, DictCursor
from yyxx_game_pkg.conf import settings
from yyxx_game_pkg.dbops.mysql_op import MysqlOperation
from yyxx_game_pkg.helpers.mysql_helper import get_dbpool
from yyxx_game_pkg.helpers.redis_helper import get_redis


class OPHelper:
    # --------------- mysql start ---------------
    @classmethod
    def connection(cls, mysql_alias="default", dict_cursor=True) -> Connection:
        db_settings = {}
        for k, v in settings.DATABASES[mysql_alias].items():
            if k == "PORT" and isinstance(v, str) and v.isdigit():  # PORT 必须为数字
                v = int(v)
            db_settings[k.lower()] = v
            if k == "NAME":
                db_settings["db"] = db_settings.pop("name")
        db_settings["cursor"] = DictCursor if dict_cursor else Cursor
        return get_dbpool(db_settings).get_connection()

    @classmethod
    def mp(cls):
        return MysqlOperation()

    @classmethod
    def sql_func_get_one(cls):
        return cls.mp().get_one

    @classmethod
    def sql_func_get_all(cls):
        return cls.mp().get_all

    # --------------- mysql end ---------------

    # --------------- redis start ---------------
    @classmethod
    def redis(cls, redis_alias="default"):
        return get_redis(settings.REDIS_SERVER[redis_alias])

    # --------------- redis end ---------------

    # --------------- redis cache start ---------------
    @classmethod
    def cache(
        cls,
        sql="",
        sql_func=None,
        redis_key="",
        ex=None,
        redis_alias="default",
        mysql_alias="default",
    ):
        """
        :param sql: sql语句
        :param sql_func: sql方法 execute get_one get_all insert
        :param redis_key: 缓存key
        :param ex: 缓存过期时间，None表示不设置过期时间
        :param redis_alias: 从redis_config中获取对应redis配置
        :param mysql_alias: 从mysql_config中获取对应mysql配置
        """
        _redis = cls.redis(redis_alias)
        data = _redis.get_data(redis_key)
        if not data:
            data = sql_func(sql, cls.connection(mysql_alias))
            if data:
                _redis.set_data(redis_key, json.dumps(str(data)), ex)

        if isinstance(data, bytes):
            data = eval(json.loads(data))

        return data

    @classmethod
    def cache_sql_one(
        cls,
        sql,
        redis_key,
        ex=None,
        redis_alias="default",
        mysql_alias="default",
    ):
        sql_func = cls.mp().get_one
        return cls.cache(sql, sql_func, redis_key, ex, redis_alias, mysql_alias)

    @classmethod
    def cache_sql_all(
        cls,
        sql,
        redis_key,
        ex=None,
        redis_alias="default",
        mysql_alias="default",
    ):
        sql_func = cls.mp().get_all
        return cls.cache(sql, sql_func, redis_key, ex, redis_alias, mysql_alias)

    # --------------- redis cache end ---------------
