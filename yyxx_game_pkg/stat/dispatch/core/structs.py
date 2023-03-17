# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/13


class ProtoSchedule(object):
    def __init__(self):
        self.SCHEDULE_NAME = None
        self.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = None
        self.SCHEDULE_CONTENT = None
        self.SCHEDULE_QUEUE_NAME = None

    def dict_str(self):
        res_dict = dict()
        res_dict["SCHEDULE_NAME"] = self.SCHEDULE_NAME
        res_dict[
            "SCHEDULE_DISPATCH_RULE_INSTANCE_NAME"
        ] = self.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME
        res_dict["SCHEDULE_CONTENT"] = self.SCHEDULE_CONTENT
        res_dict["SCHEDULE_QUEUE_NAME"] = self.SCHEDULE_QUEUE_NAME
        return res_dict

    def to_schedule(self, protocol):
        self.SCHEDULE_NAME = protocol["SCHEDULE_NAME"]
        self.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME = protocol[
            "SCHEDULE_DISPATCH_RULE_INSTANCE_NAME"
        ]
        self.SCHEDULE_CONTENT = protocol["SCHEDULE_CONTENT"]
        self.SCHEDULE_QUEUE_NAME = protocol.get("SCHEDULE_QUEUE_NAME")
        return self
