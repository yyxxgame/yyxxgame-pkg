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

    @staticmethod
    def get_celery_instance():
        """
        加载celery相关配置
        获取celery实例
        :return:
        """
        celery_name = CeleryInstance.args().name

        _app = Celery(celery_name)  # 初始化celery

        config = CeleryInstance.get_config()  # 获取配置
        _app.config_from_object(config)  # 加载配置

        CeleryInstance.TASK_REGISTER_PATH = _app.conf.get(
            "CUSTOM_TASK_REGISTER_PATH", ""
        )

        log_str = (
            f"<CeleryInstance> get_celery_instance, app_name:{celery_name}, config:{config}, publish_flag:"
            f"{config.PUBLISH_FLAG}"
        )

        root_log(log_str)
        return _app

    @staticmethod
    def args():
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
    def get_config():
        file_path = CeleryInstance.args().config

        import importlib.util

        spec = importlib.util.spec_from_file_location("*", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

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


# region celery实例化
"""
app.conf.get('worker_max_tasks_per_child', 0)
"""
app = CeleryInstance.get_celery_instance()
# endregion
