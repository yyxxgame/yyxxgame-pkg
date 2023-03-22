# -*- coding: utf-8 -*-
"""
@File: redis_helper
@Author: ltw
@Time: 2023/3/9
"""
import redis
from yyxx_game_pkg.utils.decorator import singleton_unique


def get_redis(config: dict):
    """
    缓存redis
    :return:
    """

    class Config(RedisConfig):
        """
        redis config
        """

        HOST = config["host"]
        PORT = config["port"]
        DB = config["db"]
        PASSWORD = config["password"]
        OVERDUE_SECOND = config.get("overdue_second", 86400)

    return RedisHelper(Config())


class RedisConfig:
    """
    redis config
    """

    HOST = None
    PORT = None
    DB = None
    PASSWORD = None
    OVERDUE_SECOND = 86400


@singleton_unique
class RedisHelper:
    def __init__(self, config: RedisConfig):
        connection_pool = redis.ConnectionPool(
            host=config.HOST, port=config.PORT, db=config.DB, password=config.PASSWORD
        )
        self.__r = redis.Redis(connection_pool=connection_pool)

    @property
    def redis_cli(self):
        return self.__r

    def get_data(self, key):
        return self.__r.get(key)

    def set_data(self, key, value, ex=None, _px=None):
        return self.__r.set(key, value, ex, _px)

    def list_keys(self, pattern="*"):
        return self.__r.keys(pattern)

    def delete(self, key):
        return self.__r.delete(key)

    def hset(self, name, key, value):
        return self.__r.hset(name, key, value)

    def hget(self, name, key):
        return self.__r.hget(name, key)

    def hdel(self, name, *keys):
        return self.__r.hdel(name, *keys)

    def hgetall(self, name):
        return self.__r.hgetall(name)

    def hlen(self, name):
        return self.__r.hlen(name)

    def incr(self, name, amount=1):
        return self.__r.incr(name, amount)

    def expire(self, key, ex):
        """
        设置key的过期时间
        :param key:
        :param ex:
        :return:
        """
        return self.__r.expire(key, ex)

    def lpush(self, key, *val):
        """
        在key对应的list中添加元素，每个新的元素都添加到列表的最左边
        :param key:
        :param val:
        :return:
        """
        return self.__r.lpush(key, *val)

    def rpush(self, key, *val):
        """
        同lpush，但每个新的元素都添加到列表的最右边
        :param key:
        :param val:
        :return:
        """
        return self.__r.rpush(key, *val)

    def lrange(self, key, start=0, end=-1):
        """
        分片获取元素
        :param key:
        :param start:
        :param end:
        :return:
        """
        return self.__r.lrange(key, start, end)
