# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9
import logging
import traceback

# region logic入口
from yyxx_game_pkg.xtrace.helper import get_current_trace_id

from ..common import fastapi_except_monitor
from ..core.manager import RuleManager
from ..core.structs import ProtoSchedule
from .workflows import WorkFlowMethods

logger = logging.getLogger(__name__)


@fastapi_except_monitor
def task_logic(msg):
    """
    :param msg:
    :return:
    """
    # 解析命令,构建任务标签列表
    task_sig_list = parse_task(msg)
    if not task_sig_list:
        err_msg = f"<task_logic> main_dispatch_logic, parse task failed: {traceback.format_exc()}"
        logger.info(err_msg)
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
    schedule = ProtoSchedule(schedule)
    instance_name = schedule.schedule_dispatch_rule_instance_name

    # 校验队列名
    if schedule.schedule_queue_name is None:
        logger.info("<parse_command_data> SCHEDULE_QUEUE_NAME is None, schedule: %s", schedule)
        return task_sig_list

    # 获取对应计划解析规则
    rule = RuleManager().rules.get(instance_name)
    if not rule:
        logger.info("<parse_command_data> rule is None, instance_name: %s", instance_name)
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
def _dispatch_one_task(task_sig):
    # ***************** queue 和 priority 在生成sig 时已配置*****************
    # ***************** 具体参考 RuleBase.make_signature_group *************
    common_options = {
        # "queue": queue_name,
        # "priority": 3,
        # 'serializer': 'pickle'
        "headers": {"X-Trace-ID": get_current_trace_id()},
    }
    res = task_sig.apply_async(**common_options)
    # 根据res获取task id
    task_id_list = []
    WorkFlowMethods.fill_res_task_id_list(res, task_id_list)

    return res.id, task_id_list


def dispatch_tasks(task_sig_list):
    """
    :param task_sig_list:
    :return:
    """
    task_id_list = []  # task id列表
    task_type_list = []  # task类型列表（日志显示用）
    task_queue_flag_list = []  # task队列名列表（日志显示用）
    task_cnt = 0  # task数（日志显示用）
    max_sig_cnt = 0  # 单次提交任务数峰值（日志显示用）
    for task_sig in task_sig_list:
        task_type_list.append(type(task_sig))

        queue = task_sig.options.get("queue")
        priority = task_sig.options.get("priority")
        queue_flag = f"{queue}@{priority}"
        task_queue_flag_list.append(queue_flag)

        # 获取任务数
        WorkFlowMethods.reset_max_sig_cnt()
        task_cnt += WorkFlowMethods.calculate_sig_cnt(task_sig)
        max_sig_cnt = max(WorkFlowMethods.get_max_sig_cnt(), max_sig_cnt)

        # 提交任务
        m_task_id, s_task_id_list = _dispatch_one_task(task_sig)
        task_id_list.append(m_task_id)
        logger.info(
            "<dispatch_tasks> record_task_id, queue:%s, m_task_id:%s, s_task_len:%d, s_task_id_list:%s",
            queue_flag,
            m_task_id,
            len(s_task_id_list),
            s_task_id_list,
        )

    logger.info(
        "<dispatch_tasks> dispatch_tasks, queue_name:%s, task_cnt:%s, max_sig_cnt:%s",
        task_queue_flag_list,
        task_cnt,
        max_sig_cnt,
    )
    return task_id_list


# endregion
