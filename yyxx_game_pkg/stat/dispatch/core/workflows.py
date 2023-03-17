# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9


class WorkFlowMethods(object):
    @staticmethod
    def get_task_sig_queue_name(task_sig):
        queue_flag = "queue_flag"
        from celery import chord
        from celery import group
        from celery.canvas import Signature
        from celery.canvas import _chain

        if isinstance(task_sig, chord):
            # chord
            queue_name = task_sig.tasks[0].options.get(queue_flag)
        elif isinstance(task_sig, group) or isinstance(task_sig, _chain):
            # group, chain
            sig = task_sig.tasks[0]
            return WorkFlowMethods.get_task_sig_queue_name(sig)
        elif isinstance(task_sig, Signature):
            # signature
            queue_name = task_sig.options.get(queue_flag)
        else:
            return None

        return queue_name

    @staticmethod
    def merge_sig_list(sig_list):
        if not sig_list:
            return None
        if len(sig_list) > 1:
            from celery import group

            sig_gather = group(*tuple(sig_list))
            return sig_gather
        else:
            return sig_list[0]

    @staticmethod
    def fill_res_task_id_list(res, task_id_list):
        if not res:
            return False
        from celery.result import GroupResult
        from celery.result import AsyncResult

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
        pass
        from celery import chord
        from celery.canvas import _chain
        from celery import group

        if isinstance(sig, chord):
            body_cnt = WorkFlowMethods.calculate_sig_cnt(sig.body)
            WorkFlowMethods.update_max_sig_cnt(body_cnt)
            return WorkFlowMethods.calculate_sig_cnt(sig.tasks) + body_cnt
        elif isinstance(sig, _chain):
            return WorkFlowMethods.calculate_sig_cnt(sig.tasks)
        elif isinstance(sig, group):
            cnt = WorkFlowMethods.calculate_sig_cnt(sig.tasks)
            WorkFlowMethods.update_max_sig_cnt(cnt)
            return cnt
        elif isinstance(sig, tuple):
            cnt = 0
            for s in sig:
                cnt += WorkFlowMethods.calculate_sig_cnt(s)

            WorkFlowMethods.update_max_sig_cnt(cnt)
            return cnt
        elif isinstance(sig, list):
            cnt = 0
            for s in sig:
                cnt += WorkFlowMethods.calculate_sig_cnt(s)

            return cnt
        else:
            return 1

    # endregion

    # region make sig
    @staticmethod
    def link_signatures(sig_list):
        from celery import chain

        sig = chain(tuple(sig_list))
        return sig

    @staticmethod
    def make_signature_batch(
        task_path, business_inst_name, kwargs_list=None, queue_name=None
    ):
        sig = None
        s_container = []
        if kwargs_list:
            for kwargs in kwargs_list:
                s = WorkFlowMethods._make_signature(
                    task_path, business_inst_name, **kwargs
                )
                s_container.append(s)

        # 填充队列名
        WorkFlowMethods._fill_sig_queue_name(s_container, queue_name)

        if not s_container:
            return sig

        if len(s_container) > 1:
            from celery import group

            sig = group(tuple(s_container))
            WorkFlowMethods._fill_sig_queue_name(sig, queue_name)
        else:
            sig = s_container[0]

        return sig

    @staticmethod
    def _make_signature(task_path, business_inst_name, *args, **kwargs):
        exec(f"from {task_path} import {business_inst_name}")
        return eval(business_inst_name).s(*args, **kwargs)

    @staticmethod
    def _fill_sig_queue_name(sig_list, queue_name):
        from celery import group

        if queue_name is None:
            assert False

        from yyxx_game_pkg.stat.dispatch.common.common import get_queue_name

        real_queue_name = get_queue_name(queue_name)
        if isinstance(sig_list, list):
            for s in sig_list:
                s.options["queue"] = real_queue_name
                s.options["queue_flag"] = queue_name
        elif isinstance(sig_list, group):
            sig_list.options["queue"] = real_queue_name
            sig_list.options["queue_flag"] = queue_name

    # endregion


#
# if __name__ == '__main__':
#     from logic.celery_core.task_register import add
#     s = add.s(1, 1)
#     res = s.apply_async()
#     print res
#     # from celery import group
#     # g = group(s, s)
#     # c = WorkFlowMethods.link_sig_list([g, s, g, s, s])
#     # res_g = c.apply_async()
#     # task_id_list = []
#     # WorkFlowMethods.fill_res_task_id_list(res_g, task_id_list)
#     # print task_id_list
