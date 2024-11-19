# -*- coding: utf-8 -*-#
"""
Author:       Winslen
Date:         2024/11/19
"""

import logging
from pymysql.cursors import Cursor
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine
from yyxx_game_pkg.utils.decorator import (
    except_monitor,
    log_execute_time_monitor,
    singleton_unique_obj_args,
)


@singleton_unique_obj_args
class MysqlDbEnginePool(object):
    @property
    def engine(self):
        return self.DB_POOL

    def __init__(self, config: dict):
        self.DB_POOL = create_engine(
            url=config["url"],
            pool_size=config["POOL_SIZE"],
            # 允许进入的连接数 连接池 “overflow”
            max_overflow=config["MAX_OVERFLOW"],
            pool_pre_ping=True,
            connect_args=config["CONNECT_ARGS"],
            pool_timeout=60,
            **config["EXTRA_KWARGS"],
        )
        logging.debug("<MysqlDbEnginePool> init, info:%s", config)

    @except_monitor
    @log_execute_time_monitor()
    def get_connection(self):
        return self.DB_POOL.connect()

    def close_connection(self):
        self.DB_POOL.dispose()


@singleton_unique_obj_args
class AsyncMysqlDbEnginePool(object):
    @property
    def engine(self):
        return self.DB_POOL

    def __init__(self, config: dict):
        self.DB_POOL = create_async_engine(
            url=config["url"],
            pool_size=config["POOL_SIZE"],
            # 允许进入的连接数 连接池 “overflow”
            max_overflow=config["MAX_OVERFLOW"],
            pool_pre_ping=True,
            connect_args=config["CONNECT_ARGS"],
            pool_timeout=60,
            **config["EXTRA_KWARGS"],
        )
        logging.debug("<AsyncMysqlDbEnginePool> init, info:%s", config)

    def get_connection(self):
        return self.DB_POOL.connect()

    async def close_connection(self):
        await self.DB_POOL.dispose()


def get_db_engine_pool(config: dict, drivername="mysql+pymysql", async_engine=False):
    """
    获取sqlalchemy连接池
    :param config: 配置表 (如app.conf.STAT_MYSQL_CONFIG)
    :param drivername: 使用的驱动
    :param async_engine: 是否异步
    :return:
    """
    conf = {
        "url": URL.create(
            drivername=drivername,
            username=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=config["db"],
        ),
        "USE_UNICODE": config.get("use_unicode", True),
        "POOL_SIZE": config.get("mincached", 5),
        "MAX_OVERFLOW": config.get("maxconnections", 50) - config.get("mincached", 5),
        "CONNECT_ARGS": {
            "charset": config.get("charset", "utf8"),
            "cursorclass": config.get("cursor", Cursor),
            "use_unicode": config.get("use_unicode", True),
        },
        "EXTRA_KWARGS": {**config.get("extra_kwargs", {})},
    }
    if async_engine:
        return AsyncMysqlDbEnginePool(conf)
    return MysqlDbEnginePool(conf)
