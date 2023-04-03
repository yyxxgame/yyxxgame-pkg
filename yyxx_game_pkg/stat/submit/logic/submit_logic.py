# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/15
from yyxx_game_pkg.utils.xdate import split_date_str_by_day
from yyxx_game_pkg.logger.log import root_log


__schedule_file_path = "None"
__api_addr = "http://localhost:8080"


# region 内部方法
def _to_protocol_by_schedule(
    schedule, is_work_flow=False, custom_content=None, custom_queue=None
):
    proto_dict = dict()
    schedule_name = schedule.SCHEDULE_NAME
    instance_name = schedule.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME
    queue_name = (
        schedule.SCHEDULE_QUEUE_NAME
        if hasattr(schedule, "SCHEDULE_QUEUE_NAME")
        else None
    )
    if custom_queue is not None:
        queue_name = custom_queue

    import copy

    content = copy.deepcopy(schedule.SCHEDULE_CONTENT)
    if custom_content:
        for c in content:
            if not isinstance(c, dict) or not isinstance(custom_content, dict):
                continue
            content_dict = c.get("custom_content")
            if not content_dict:
                c.update(custom_content)
            else:
                data_dict = custom_content.get("custom_content")
                content_dict.update(data_dict)

    proto_dict["SCHEDULE_NAME"] = schedule_name
    proto_dict["SCHEDULE_DISPATCH_RULE_INSTANCE_NAME"] = instance_name
    if queue_name:
        proto_dict["SCHEDULE_QUEUE_NAME"] = queue_name

    if is_work_flow:
        dict_rule = dict()
        for schedule_param in content:
            group = schedule_param.get("group")
            step = schedule_param.get("step")
            custom_content = schedule_param.get("custom_content")
            sub_schedule_name = schedule_param.get("schedule")
            if step is None or sub_schedule_name is None:
                continue
            if group is None:
                group = 1
            if not dict_rule.get(group):
                dict_rule[group] = dict()

            if not dict_rule[group].get(step):
                dict_rule[group][step] = []
            schedule_str = to_protocol(
                sub_schedule_name,
                custom_content=custom_content,
                custom_queue=queue_name,
            )
            dict_rule[group][step].append(schedule_str)
        content = dict_rule

    proto_dict["SCHEDULE_CONTENT"] = content

    return proto_dict


def _get_schedule(schedule_name):
    import importlib

    schedule_dir = "schedule"
    if schedule_name.find("@") > -1:
        schedule_name, schedule_dir = schedule_name.split("@")

    schedule = None
    is_work_flow = False
    try:
        module = f"{__schedule_file_path}.{schedule_dir}.statistic_task.{schedule_name}"
        schedule = importlib.import_module(module)
        is_work_flow = (
            schedule.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME.find("work_flow") >= 0
        )
    except Exception as e:
        try:
            module = f"{__schedule_file_path}.{schedule_dir}.work_flow.{schedule_name}"
            schedule = importlib.import_module(module)
            is_work_flow = True
        except Exception as e:
            root_log(e)

    return schedule, is_work_flow


def _parse_proto_dict(proto_dict):
    process_proto_list = []
    schedule_name = proto_dict.get("SCHEDULE_DISPATCH_RULE_INSTANCE_NAME")

    if schedule_name.find("work_flow") >= 0:
        schedule_content = proto_dict.get("SCHEDULE_CONTENT")
        step_schedule_content = schedule_content[1][1][0].get("SCHEDULE_CONTENT")[0]
        date_interval = step_schedule_content.get("day_interval")
        if date_interval and date_interval == "SPLIT_DATE_BY_DAY":
            date_appoint = step_schedule_content["date_appoint"]
            date_list = split_date_str_by_day(date_appoint[0], date_appoint[1])
            for date_offset in date_list:
                content_k_v = dict()
                content_k_v["date_appoint"] = ""
                content_k_v["day_interval"] = date_offset
                _modify_proto_content(schedule_content, content_k_v)
                process_proto_list.append(proto_dict)
        else:
            process_proto_list.append(proto_dict)
    else:
        process_proto_list.append(proto_dict)

    return process_proto_list


def _modify_proto_content(schedule_content, content_key_value):
    if not isinstance(schedule_content, dict) or not isinstance(
        content_key_value, dict
    ):
        return
    for content_dict in schedule_content.values():  # 替换工作流content的key, value
        for key, content_list in content_dict.items():
            temp_list = []
            for content in content_list:
                content = content
                for con_key, con_value in content_key_value.items():
                    if con_key == "SCHEDULE_QUEUE_NAME":
                        content[con_key] = con_value
                    else:
                        s_content = content["SCHEDULE_CONTENT"]
                        for c in s_content:
                            c[con_key] = con_value
                temp_list.append(content)
            content_dict[key] = temp_list


# endregion

# region 外部方法
def set_config(path: str, api_addr: str):
    global __schedule_file_path, __api_addr
    __schedule_file_path = path
    __api_addr = api_addr


def to_protocol(schedule_name, custom_content=None, custom_queue=None):
    schedule, is_work_flow = _get_schedule(schedule_name)
    if not schedule:
        return None
    return _to_protocol_by_schedule(
        schedule, is_work_flow, custom_content, custom_queue
    )


def process_proto(proto_dict):
    res_list = []

    # 工作流切割
    process_proto_list = _parse_proto_dict(proto_dict)

    for p in process_proto_list:
        res_list.append(p)

    return res_list


def send(proto):
    import requests

    url = f"{__api_addr}/submit"
    post_data = {"content": proto}
    res = requests.post(json=post_data, url=url, timeout=600)
    return res


# endregion
