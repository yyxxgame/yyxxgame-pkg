# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9
from celery import chord, group, signature
from celery.canvas import _chain
from celery.result import AsyncResult, GroupResult


class WorkFlowMethods:
    """
    WorkFlowMethods
    """

    @staticmethod
    def link_task_s(**options):
        """
        link_task 连接任务流, 接收上一步骤结果传递给下一步骤
        原因: 工作流chain多个group时 celery会自动升级为chord, chord的body步骤会接收每个header步骤的运行结果
        如: chain(
            group(task1, task2),
            group(task3, task4),
            group(task5, task6)
        )
        以task.add为例, 生成sig为:
            %celery.group([task_register.add(1), task_register.add(2)],
                tasks=[task_register.add(3), task_register.add(4)]) | group([task_register.add(5), add(6)])
            前两个group被合并成chord的header, 最后的group被当成chord的body
            这并不是我们期望的
        所以在构建任务时将group转换为chord, 该函数作为chord的body, 用于接收group的运行结果
        上面的任务将group改为chord后为:
            chain(
                chord(group(task1, task2), link_task),
                chord(group(task3, task4), link_task),
                chord(group(task5, task6), link_task)
            )
        生成的sig为:
           %(task_register.link_task([add(1), add(2)]) | %(link_task([add(3), add(4)]) | %link_task([add(5), add(6)])))
        可以看到是符合我们预期的
        根据不同需求会将link_task设置为immutable, 无需传递结果
        :return:
        """
        from celery import current_app as app

        task_path = app.conf.get("CUSTOM_TASK_REGISTER_PATH")
        sig = signature(f"{task_path}.link_task")
        sig.options.update(options)
        return sig

    @staticmethod
    def fill_res_task_id_list(res, task_id_list):
        if not res:
            return False

        if isinstance(res, GroupResult):
            # GroupResult
            for res_ in res.results:
                task_id_list.append(res_.task_id)
        elif isinstance(res, AsyncResult):
            # AsyncResult
            task_id_list.append(res.task_id)
        else:
            return False

        if res.parent is not None:
            WorkFlowMethods.fill_res_task_id_list(res.parent, task_id_list)

        return True

    # region Signature Statistic
    max_sig_cnt = 0

    @staticmethod
    def reset_max_sig_cnt():
        WorkFlowMethods.max_sig_cnt = 0

    @staticmethod
    def get_max_sig_cnt():
        return WorkFlowMethods.max_sig_cnt

    @staticmethod
    def update_max_sig_cnt(cnt):
        WorkFlowMethods.max_sig_cnt = max(WorkFlowMethods.max_sig_cnt, cnt)

    @staticmethod
    def calculate_sig_cnt(sig):
        """
        计算sig包含task数量
        :param sig:
        :return:
        """
        if isinstance(sig, chord):
            body_cnt = WorkFlowMethods.calculate_sig_cnt(sig.body)
            WorkFlowMethods.update_max_sig_cnt(body_cnt)
            return WorkFlowMethods.calculate_sig_cnt(sig.tasks) + body_cnt
        if isinstance(sig, _chain):
            return WorkFlowMethods.calculate_sig_cnt(sig.tasks)
        if isinstance(sig, group):
            cnt = WorkFlowMethods.calculate_sig_cnt(sig.tasks)
            WorkFlowMethods.update_max_sig_cnt(cnt)
            return cnt
        if isinstance(sig, tuple):
            cnt = 0
            for _s in sig:
                cnt += WorkFlowMethods.calculate_sig_cnt(_s)

            WorkFlowMethods.update_max_sig_cnt(cnt)
            return cnt
        if isinstance(sig, list):
            cnt = 0
            for _s in sig:
                cnt += WorkFlowMethods.calculate_sig_cnt(_s)

            return cnt
        return 1
