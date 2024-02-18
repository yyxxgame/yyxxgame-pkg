# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

"""
celery 实例入口
"""
import argparse
import logging

from celery import Celery


class CeleryInstance:
    """
    celery 接口
    """

    # region external
    @staticmethod
    def get_celery_instance():
        """
        加载celery相关配置
        获取celery实例
        :return:
        """
        celery_name = CeleryInstance._args().name

        _app = Celery(celery_name)  # 初始化celery

        _app.config_from_envvar("CELERY_CONFIG_MODULE")  # 加载配置

        conf_jaeger = _app.conf.get("JAEGER")
        if conf_jaeger:
            from opentelemetry.instrumentation.celery import CeleryInstrumentor
            from opentelemetry.instrumentation.requests import RequestsInstrumentor
            from yyxx_game_pkg.xtrace.helper import register_to_jaeger

            if celery_name:
                conf_jaeger["service_name"] += f"-{celery_name}"

            register_to_jaeger(**conf_jaeger)
            CeleryInstrumentor().instrument()
            RequestsInstrumentor().instrument()

        log_str = f"<CeleryInstance> get_celery_instance, app_name:{celery_name}, publish_flag:{_app.conf.get('PUBLISH_FLAG')}"
        logging.info(log_str)
        return _app

    @staticmethod
    def get_current_task_id():
        """
        当前task id [如果有]
        :return:
        """
        from celery import current_task

        try:
            return current_task.request.id
        except:
            return -1

    # endregion

    # region inner
    @staticmethod
    def _args():
        """
        argparse
        -n 服务名
        -c 配置文件
        :return:
        """
        parser = argparse.ArgumentParser(allow_abbrev=False)
        parser.add_argument("-n", "--name")
        args = parser.parse_known_args()
        return args[0]

    # endregion


# region celery实例化
"""
app.conf.get('worker_max_tasks_per_child', 0)
"""
# app = CeleryInstance.get_celery_instance()
# endregion
