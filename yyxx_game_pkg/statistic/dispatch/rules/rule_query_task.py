# -*- coding: utf-8 -*-
"""
@File: rule_query_task
"""

import copy
import datetime
from typing import AnyStr, Dict, List, Tuple

from celery import current_app as app

from yyxx_game_pkg.helpers.redis_helper import get_redis
from yyxx_game_pkg.utils.xListStr import split_list_ex

from ..core.manager import rule_register
from .rule_base import ProtoSchedule
from .rule_statistic_task import RuleStatisticTaskLogic


class RuleQueryTaskLogic(RuleStatisticTaskLogic):
    """
    RuleQueryTaskLogic
    """

    def build_sig_logic(self, schedule: ProtoSchedule):
        schedule_info = {"schedule_name": schedule.schedule_name}
        schedule_info.update(schedule.schedule_content)
        sql_md5 = schedule_info.get("sql_md5")
        if not sql_md5:
            raise ValueError("sql_md5 is Empty")
        inst_name = schedule.schedule_dispatch_rule_instance_name
        if not inst_name:
            inst_name = self.inst_name
        schedule_info.update({"instance_name": inst_name})
        # 根据md5获取查询参数
        query_params = self.__get_query_params(sql_md5)

        # center 传过来可能是空字符串 '' 此处做转换
        _d_params = query_params.get("dispatch_params")
        query_params["dispatch_params"] = _d_params if isinstance(_d_params, dict) else {}

        # 参数赋值
        schedule_info.update(query_params)

        # 构建查询参数列表
        task_kwargs_list = self.__make_task_kwargs_list(schedule_info)

        # 构建signature
        sig = self.make_signature_group(
            app.conf.get("CUSTOM_TASK_REGISTER_PATH"),
            inst_name,
            schedule.queue,
            schedule.priority,
            task_kwargs_list,
        )
        return sig

    # region 内部方法
    @staticmethod
    def __get_query_params(sql_md5):
        """
        从redis中获取完整的查询参数
        :param sql_md5:
        :return:
        """
        redis_handle = get_redis(app.conf.get("REDIS_CONFIG"))
        query_param = redis_handle.get_data(sql_md5)
        return eval(query_param)

    @staticmethod
    def __make_task_kwargs_list(schedule_info):
        dispatch_params = schedule_info.get("dispatch_params")
        # dispatch_params = {"date_split_by": "1:day", "list_cond_split_by": "5:op_gcids"}
        if not dispatch_params:
            return [schedule_info]
        instance_name = schedule_info.get("instance_name")
        # collect 任务不切分
        if instance_name.find("collect") > -1:
            return [schedule_info]

        # split_by_date 1*month, 3*day, 2*hour, 10*minute
        # 仅支持单条件
        date_split_by = dispatch_params.get("date_split_by")
        split_date_list = RuleQueryTaskLogic.split_by_date(schedule_info, date_split_by)

        # cond_split_by 10*server_ids, 2*op_gcids
        # 仅支持单条件 (多条件下任务数量指数增长，不好控制，限制单条件)
        list_cond_split_by = dispatch_params.get("list_cond_split_by")
        split_list_cond_list = RuleQueryTaskLogic.split_by_list_cond(schedule_info, list_cond_split_by)

        info_dict_list = []
        for sdate, edate in split_date_list:
            _schedule_info = copy.deepcopy(schedule_info)
            _schedule_info["sdate"] = [sdate]
            _schedule_info["edate"] = [edate]
            if not split_list_cond_list:
                info_dict_list.append(_schedule_info)
                continue
            for cond_key, cond_list in split_list_cond_list.items():
                for _list_cond in cond_list:
                    _schedule_info = copy.deepcopy(_schedule_info)
                    _schedule_info[cond_key] = _list_cond
                    info_dict_list.append(_schedule_info)
        return info_dict_list

    # endregion

    @staticmethod
    def split_by_date(schedule_info, split_by=None) -> List[Tuple[AnyStr, AnyStr]]:
        """
        split_date_str_by_day
        """
        sdate_str = schedule_info["sdate"][0]
        edate_str = schedule_info["edate"][0]
        if not split_by:
            return [(sdate_str, edate_str)]

        if not (sdate_str and edate_str):
            return []
        res_list = []
        size, time_unit = split_by.lower().split("*")
        size = int(size)
        if time_unit == "day":
            interval = datetime.timedelta(days=size)
        elif time_unit == "hour":
            interval = datetime.timedelta(hours=size)
        elif time_unit == "minute":
            interval = datetime.timedelta(minutes=size)
        else:
            raise ValueError("""<RuleQueryTaskLogic.split_by_date>不支持的切分单位("1:day", "3:hour", "10:minute")""")
        # 按时间切分
        start_dt = datetime.datetime.strptime(sdate_str, "%Y-%m-%d %H:%M:%S")
        edate_str = edate_str.replace("00:00:00", "23:59:59")
        end_dt = datetime.datetime.strptime(edate_str, "%Y-%m-%d %H:%M:%S")
        offset = datetime.timedelta(seconds=1)
        while start_dt < end_dt:
            next_dt = min((start_dt + interval - offset), end_dt)
            res_list.append(
                (
                    start_dt.strftime("%Y-%m-%d %H:%M:%S"),
                    next_dt.strftime("%Y-%m-%d %H:%M:%S"),
                )
            )
            start_dt = next_dt + offset

        return res_list

    @staticmethod
    def split_by_list_cond(schedule_info, cond_split_by) -> Dict[str, List]:
        if not cond_split_by:
            return {}
        size, cond_key = cond_split_by.strip().split("*")
        key_cond_list = schedule_info.get(cond_key)
        if not key_cond_list:
            return {}
        _cond_list = split_list_ex(key_cond_list, int(size))
        return {cond_key: _cond_list}


@rule_register(inst_name_list=["query_task_instance", "query_collect_instance"])
class RuleQueryTask(RuleQueryTaskLogic):
    """
    RuleQueryTask
    """
