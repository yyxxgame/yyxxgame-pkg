# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2022/2/16
import json
import logging
import os

from celery.schedules import crontab


class TaskLoader:
    """
    task配置加载类
    """

    TASK = "task_register.crontab_task_instance"  # 注册任务路径

    # submit脚本路径（获取绝对路径）
    SUBMIT_SH = "python /data/www/submit/submit.py"

    def __init__(self):
        pass

    def load(self):
        """
        加载任务配置文件
        :return:
        """
        cron = {}

        # 测试任务
        cron.update(self.__load("task/task_test.json"))
        #
        # # 加载分钟任务
        # cron.update(self.__load("task/task_minute.json"))
        #
        # # 加载小时任务
        # cron.update(self.__load("task/task_hour.json"))
        #
        # # 加载天任务
        # cron.update(self.__load("task/task_day.json"))

        return cron

    def __load(self, json_file_name):
        from celery import current_app

        cron = {}
        file_path = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(file_path, json_file_name)
        with open(file_path, "r", encoding="utf8") as file_json:
            json_task = json.load(file_json)
            task_list = json_task["task"]
            for _t in task_list:
                data = {}

                schedule = _t["schedule"]
                interval = _t["interval"]
                task_name = f"task_{schedule}_{interval}"

                time_member = interval.split(" ")
                assert len(time_member) == 5
                _c = crontab(
                    minute=time_member[0],
                    hour=time_member[1],
                    day_of_week=time_member[2],
                    day_of_month=time_member[3],
                    month_of_year=time_member[4],
                )

                data["task"] = self.TASK
                data["schedule"] = _c
                data["kwargs"] = {"cmd": f"{self.SUBMIT_SH} -s {schedule}"}
                data["options"] = {"queue": current_app.conf.CRONTAB_QUEUE}
                cron[task_name] = data
                logging.info("<TaskLoader.__load> load data: %s", data)
            logging.info("<TaskLoader.__load> %s load task cnt: %s", json_file_name, len(task_list))
            file_json.close()

        return cron
