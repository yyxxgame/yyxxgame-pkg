# -*- coding: utf-8 -*-
"""
@File: structs
@Author: ltw
@Time: 2023/12/28
"""


class ProtoSchedule:
    """
    ProtoSchedule
    """

    def __init__(self, schedule):
        self.schedule = schedule

    @property
    def schedule_name(self):
        """
        :return:
        """
        return self.schedule["SCHEDULE_NAME"]

    @property
    def schedule_dispatch_rule_instance_name(self):
        """
        :return:
        """
        return self.schedule["SCHEDULE_DISPATCH_RULE_INSTANCE_NAME"]

    @property
    def schedule_content(self):
        """
        :return:
        """
        return self.schedule["SCHEDULE_CONTENT"]

    @property
    def schedule_queue_name(self):
        """
        :return:
        """
        # 必填项
        schedule_queue_name = self.schedule.get("SCHEDULE_QUEUE_NAME")
        if schedule_queue_name is None:
            raise ValueError("SCHEDULE_QUEUE_NAME is None")
        return schedule_queue_name

    @property
    def queue(self):
        """
        :return:
        """
        # 必填项
        return self.schedule_queue_name.split("@")[0]

    @property
    def priority(self):
        """
        :return:
        """
        try:
            return int(self.schedule_queue_name.split("@")[1])
        except IndexError as _:
            return 3

    def dict_str(self):
        """
        :return:
        """
        res_dict = {
            "SCHEDULE_NAME": self.schedule_name,
            "SCHEDULE_DISPATCH_RULE_INSTANCE_NAME": self.schedule_dispatch_rule_instance_name,
            "SCHEDULE_CONTENT": self.schedule_content,
            "SCHEDULE_QUEUE_NAME": self.schedule_queue_name,
        }
        return str(res_dict)
