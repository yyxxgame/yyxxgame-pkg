# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9


def main_dispatch_logic(msg, *args, **kwargs):
    # 日志打印
    log_str = "<DispatchRulesManagerLogic> main_dispatch_logic, data_len:{}, detail:{}".format(
        len(msg), msg[0 : min(len(msg) - 1, 1024)]
    )
    local_log(log_str)

    # 解析命令,构建任务标签列表
    task_sig_list = parse_command_data(msg)
    if not task_sig_list:
        local_log(
            "<DispatchRulesManagerLogic> main_dispatch_logic, command error; {}".format(
                traceback.format_exc()
            )
        )
        assert False

    # 分发任务
    return dispatch_tasks(task_sig_list)


# region 任务分发
@log_execute_time_monitor()
def _dispatch_one_task(task_sig, queue_priority, queue_name=None):
    common_options = {
        "priority": queue_priority,
        # 'serializer': 'pickle'
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

    # # 记录结果集
    # push_task_res(queue_name if queue_name else 'celery', res)


def dispatch_tasks(task_sig_list):
    task_id_list = []  # task id列表
    task_type_list = []  # task类型列表（日志显示用）
    task_queue_flag_list = []  # task队列名列表（日志显示用）
    task_cnt = 0  # task数（日志显示用）
    max_sig_cnt = 0  # 单次提交任务数峰值（日志显示用）
    for task_sig in task_sig_list:
        task_type_list.append(type(task_sig))

        # 获取queue_flag
        # from dispatch_svc.schedule.work_flow_methods import WorkFlowMethods

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
            f"<DispatchRulesManagerLogic> record_task_id, queue:{queue_name}, "
            f"priority:{queue_priority}, m_task_id:{m_task_id}, "
            f"s_task_len:{len(s_task_id_list)}, s_task_id_list:{s_task_id_list}"
        )

    local_log(
        f"<DispatchRulesManagerLogic> dispatch_tasks, queue_name:{task_queue_flag_list} "
        f"task_cnt:{task_cnt}, max_sig_cnt:{max_sig_cnt}, task_dispatch_cnt:{mgr.task_execute_cnt()}"
    )
    return task_id_list


# endregion
