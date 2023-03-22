# -*- coding: utf-8 -*-
"""
@File: pika_helper
@Author: ltw
@Time: 2023/3/9
"""
import pika


def get_pika(config: dict):
    """
    获取pika_conn
    :param config:
    :return:
    """

    class Config(PikaConfig):
        """
        pika config
        """

        USER = config["user"]
        PASSWORD = config["password"]
        HOST = config["host"]
        PORT = config["port"]
        M_PORT = config["m_port"]
        V_HOST = config["v_host"]
        HEARTBEAT = config["heartbeat"]
        TIMEOUT = config["timeout"]

    return pika_conn(Config())


class PikaConfig:
    """
    pika config
    """

    USER = None
    PASSWORD = None
    HOST = None
    PORT = None
    M_PORT = None
    V_HOST = None
    HEARTBEAT = None
    TIMEOUT = None


def pika_conn(config: PikaConfig):
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
