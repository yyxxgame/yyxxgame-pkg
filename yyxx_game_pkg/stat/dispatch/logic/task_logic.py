# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9
import traceback

from yyxx_game_pkg.stat.dispatch.common.common import fastapi_except_monitor
from yyxx_game_pkg.stat.dispatch.common.log import local_log
from yyxx_game_pkg.stat.dispatch.core.manager import RuleManager
from yyxx_game_pkg.stat.dispatch.core.structs import ProtoSchedule
from yyxx_game_pkg.stat.dispatch.core.workflows import WorkFlowMethods


# region logic入口
from yyxx_game_pkg.xtrace.helper import get_current_trace_id


@fastapi_except_monitor
def task_logic(msg):
    # 解析命令,构建任务标签列表
    task_sig_list = parse_task(msg)
    if not task_sig_list:
        err_msg = f"<task_logic> main_dispatch_logic, parse task failed: {traceback.format_exc()}"
        local_log(err_msg)
        return []

    # 分发任务
    return dispatch_tasks(task_sig_list)


# endregion


# region 任务解析
def parse_task(schedule):
    """
    解析命令
    :param schedule:
    :return:
    """
    task_sig_list = []

    # 反序列化
    schedule = ProtoSchedule().to_schedule(schedule)
    instance_name = schedule.SCHEDULE_DISPATCH_RULE_INSTANCE_NAME

    # 校验队列名
    if schedule.SCHEDULE_QUEUE_NAME is None:
        local_log(
            f"<parse_command_data> SCHEDULE_QUEUE_NAME is None, schedule:{schedule}"
        )
        return task_sig_list

    # 获取对应计划解析规则
    rule = RuleManager().rules.get(instance_name)
    if not rule:
        local_log(f"<parse_command_data> rule is None, instance_name:{instance_name}")
        return task_sig_list

    # 构建signature列表
    schedule_sig = rule.build(schedule)
    if not schedule_sig:
        return task_sig_list

    # link
    if isinstance(schedule_sig, list):
        task_sig_list.extend(schedule_sig)
    else:
        task_sig_list.append(schedule_sig)

    return task_sig_list


# endregion


# region 任务分发
def _dispatch_one_task(task_sig, queue_priority, queue_name=None):
    common_options = {
        "priority": queue_priority,
        # 'serializer': 'pickle'
        "headers": {"X-Trace-ID": get_current_trace_id()},
    }
    if queue_name is not None:
        # 强制指定队列名
        res = task_sig.apply_async(queue=queue_name, **common_options)
    else:
        # 动态队列名
        res = task_sig.apply_async(**common_options)

    # 根据res获取task id
    task_id_list = []

    WorkFlowMethods.fill_res_task_id_list(res, task_id_list)

    return res.id, task_id_list


def dispatch_tasks(task_sig_list):
    task_id_list = []  # task id列表
    task_type_list = []  # task类型列表（日志显示用）
    task_queue_flag_list = []  # task队列名列表（日志显示用）
    task_cnt = 0  # task数（日志显示用）
    max_sig_cnt = 0  # 单次提交任务数峰值（日志显示用）
    for task_sig in task_sig_list:
        task_type_list.append(type(task_sig))

        queue_flag = WorkFlowMethods.get_task_sig_queue_name(task_sig)
        task_queue_flag_list.append(queue_flag)

        # 解析queue_flag，获取队列名和优先级
        queue_name, queue_priority = _parse_queue_flag(queue_flag)

        # 获取任务数
        WorkFlowMethods.reset_max_sig_cnt()
        task_cnt += WorkFlowMethods.calculate_sig_cnt(task_sig)
        max_sig_cnt = max(WorkFlowMethods.get_max_sig_cnt(), max_sig_cnt)

        # 提交任务
        m_task_id, s_task_id_list = _dispatch_one_task(task_sig, queue_priority)
        task_id_list.append(m_task_id)
        local_log(
            f"<dispatch_tasks> record_task_id, queue:{queue_name}, "
            f"priority:{queue_priority}, m_task_id:{m_task_id}, "
            f"s_task_len:{len(s_task_id_list)}, s_task_id_list:{s_task_id_list}"
        )

    local_log(
        f"<dispatch_tasks> dispatch_tasks, queue_name:{task_queue_flag_list} "
        f"task_cnt:{task_cnt}, max_sig_cnt:{max_sig_cnt}"
    )
    return task_id_list


def _parse_queue_flag(queue_flag):
    """
    解析队列名标识
    :param queue_flag:
    :return:
    """
    default_priority = 3  # 默认队列优先级
    if queue_flag is None:
        # assert False
        return [None], default_priority

    res_list = queue_flag.split("@")
    queue_name = res_list[0]
    priority = min(int(res_list[1]), 10) if len(res_list) > 1 else default_priority
    return queue_name, priority


# endregion
