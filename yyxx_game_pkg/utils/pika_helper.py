# -*- coding: utf-8 -*-
"""
@File: pika_helper
@Author: ltw
@Time: 2023/3/9
"""
import pika


class PikaConfig:
    """
    pika config
    """
    USER = None
    PASSWORD = None
    HOST = None
    PORT = 5672
    M_PORT = 15672
    V_HOST = "/"
    HEARTBEAT = 600
    TIMEOUT = 3600


def connection(config):
    """
    获取rabbitmq 连接
    params: config: PikaConfig obj
    :return: pika.BlockingConnection
    """
    credentials = pika.PlainCredentials(config.USER, config.PASSWORD)
    params = pika.ConnectionParameters(
        config.HOST,
        config.PORT,
        config.V_HOST,
        credentials,
        heartbeat=config.HEARTBEAT,
        blocked_connection_timeout=config.TIMEOUT,
    )
    conn = pika.BlockingConnection(params)
    return conn
