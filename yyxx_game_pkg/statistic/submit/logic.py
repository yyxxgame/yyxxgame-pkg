# -*- coding: utf-8 -*-
"""
@File: logic
@Author: ltw
@Time: 2024/1/2
"""
import copy
import importlib

import requests

__schedule_file_path = "None"
__api_addr = "http://localhost:8080"


# region 内部方法
def _to_protocol_by_schedule(schedule):
    instance_name = schedule.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME
    queue_name = schedule.SCHEDULE_QUEUE_NAME
    proto_dict = {
        "SCHEDULE_NAME": schedule.SCHEDULE_NAME,
        "SCHEDULE_DISPATCH_RULE_INSTANCE_NAME": instance_name,
        "SCHEDULE_QUEUE_NAME": queue_name,
    }
    content_list = copy.deepcopy(schedule.SCHEDULE_CONTENT)
    schedule_content = {}
    for content in content_list:
        sub_schedule_name = content.get("schedule", "")
        # ************************** 没有子schedule 判断为单任务 start **************************
        if not sub_schedule_name:
            schedule_content = content
            break
        # ************************** 没有子schedule 判断为单任务  end  **************************
        group = content.get("group", 1)
        step = content.get("step", 1)
        if group not in schedule_content:
            schedule_content[group] = {}
        if step not in schedule_content[group]:
            schedule_content[group][step] = []
        sub_custom_content = content.get("custom_content", "")
        if not sub_custom_content:
            # 无 custom_content, 根据 schedule name 尝试解析
            sub_proto_dict = process_schedule(sub_schedule_name)
            schedule_content[group][step].append(sub_proto_dict)
            continue
        # ****************** 新增多任务配置项 rule_instance ******************
        # 必须手动指定任务实际instance
        sub_instance_name = content.get("rule_instance", instance_name)
        sub_proto_dict = {
            "SCHEDULE_NAME": sub_schedule_name,
            "SCHEDULE_DISPATCH_RULE_INSTANCE_NAME": sub_instance_name,
            "SCHEDULE_QUEUE_NAME": queue_name,
            "SCHEDULE_CONTENT": sub_custom_content,
        }
        schedule_content[group][step].append(sub_proto_dict)
    proto_dict["SCHEDULE_CONTENT"] = schedule_content
    return proto_dict


def _get_schedule(schedule_name: str):
    schedule_dir = "schedule"
    if schedule_name.find("@") > -1:
        schedule_name, schedule_dir = schedule_name.split("@")

    module = f"{__schedule_file_path}.{schedule_dir}.{schedule_name}"
    schedule = importlib.import_module(module)
    return schedule


# endregion


# region 外部方法
def set_config(path: str, api_addr: str):
    global __schedule_file_path, __api_addr
    __schedule_file_path = path
    __api_addr = api_addr


def process_schedule(schedule_name: str):
    """
    schedule 文件解析为 proto_dict
    :param schedule_name:
    :return:
    """
    schedule = _get_schedule(schedule_name)
    if not schedule:
        return None
    proto_dict = _to_protocol_by_schedule(schedule)
    return proto_dict


def send(proto: dict):
    """
    发送 proto 给服务器
    :param proto:
    :return:
    """
    url = f"{__api_addr}/submit"
    post_data = {"content": proto}
    res = requests.post(json=post_data, url=url, timeout=600)
    return res


# endregion
