# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9
from celery import chord, group
from celery.canvas import _chain
from celery.result import AsyncResult, GroupResult


class WorkFlowMethods(object):
    """
    WorkFlowMethods
    """

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
