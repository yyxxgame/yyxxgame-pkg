# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

"""
celery 实例入口
"""
import argparse
from celery import Celery

from yyxx_game_pkg.logger.log import root_log


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

        config = CeleryInstance._get_config()  # 获取配置
        _app.config_from_object(config)  # 加载配置

        conf_jaeger = _app.conf.get("JAEGER")
        if conf_jaeger:
            from opentelemetry.instrumentation.celery import CeleryInstrumentor
            from yyxx_game_pkg.xtrace.helper import register_to_jaeger

            register_to_jaeger(**conf_jaeger)
            CeleryInstrumentor().instrument()
            root_log(f"<CeleryInstance> tracer on, jaeger:{conf_jaeger}")

        log_str = (
            f"<CeleryInstance> get_celery_instance, app_name:{celery_name}, config:{config}, publish_flag:"
            f"{config.PUBLISH_FLAG}"
        )
        root_log(log_str)
        return _app

    @staticmethod
    def get_current_task_id():
        """
        当前task id [如果有]
        :return:
        """
        try:
            return app.current_task.request.id
        finally:
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
        parser.add_argument("-c", "--config")
        args = parser.parse_known_args()
        return args[0]

    @staticmethod
    def _get_config():
        file_path = CeleryInstance._args().config

        import importlib.util

        spec = importlib.util.spec_from_file_location("*", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    # endregion


# region celery实例化
"""
app.conf.get('worker_max_tasks_per_child', 0)
"""
app = CeleryInstance.get_celery_instance()
# endregion
