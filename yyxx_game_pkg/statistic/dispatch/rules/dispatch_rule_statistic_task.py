# -*- coding: utf-8 -*-
"""
@File: dispatch_rule_statistic_task
@Author: ltw
@Time: 2023/12/28
"""

import copy
import datetime
import logging
import random
from math import sqrt

from celery import current_app as app
from yyxx_game_pkg.dbops.mysql_op import MysqlOperation
from yyxx_game_pkg.helpers.mysql_helper import get_dbpool
from yyxx_game_pkg.utils.xdate import split_date_str_by_day
from yyxx_game_pkg.utils.xListStr import split_list

from ..core.manager import rule_register
from .rule_base import ProtoSchedule, RuleBase


class DispatchRuleStatisticTaskLogic(RuleBase):
    """
    DispatchRuleStatisticTaskLogic
    """

    def build(self, schedule: ProtoSchedule):
        """
        :param schedule:
        :return:
        """
        sig = self.build_sig_logic(schedule)
        return sig

    def build_sig_logic(self, schedule):
        """
        构建单任务
        :param schedule:
        :return:
        """
        schedule_name = schedule.schedule_name
        queue_name = schedule.schedule_queue_name
        content = schedule.schedule_content
        inst_name = schedule.schedule_dispatch_rule_instance_name
        if not inst_name:
            inst_name = self.inst_name
        auth_info = ""
        # 构建计划内容
        content_info = self._make_content_info(content, schedule_name, queue_name)
        if not content_info:
            return None

        # 切割任务内容
        param_list = self.__split_content_info(content_info)
        if not param_list:
            return None

        logging.info(
            "<DispatchRule> build_sig_logic,schedule_name:%s, "
            "auth: %s, queue_name:%s, stat_ids:%s, task_len:%d, param:%s",
            schedule_name,
            auth_info,
            queue_name,
            content_info["statistic_ids"],
            len(param_list),
            param_list[0],
        )

        # 构建signature
        sig = self.make_signature_group(
            app.conf.get("CUSTOM_TASK_REGISTER_PATH"),
            inst_name,
            schedule.queue,
            schedule.priority,
            kwargs_list=param_list,
        )
        if not sig:
            return None
        return sig

    def _make_content_info(self, content, schedule_name, queue_name):
        # 获取日期区间
        date_interval = self.__parse_date_interval(content)

        # 额外参数
        ex_params = content.get("ex_params", {})

        # 获取server_ids
        server_ids = self.__parse_server_ids(content)
        if not server_ids:
            logging.info("<DispatchRule> appoint_server_ids is None, content:%s", content)
            status = ex_params.get("status", "")
            server_ids = self.get_all_server_ids(status)

        # server_ids 切片
        server_id_slice_size = content.get("server_id_slice_size", -1)

        # 获取statistic_ids
        statistic_ids = self.__parse_statistic_ids(content)
        # statistic_ids 切分
        statistic_ids_slice_size = content.get("statistic_ids_slice_size", -1)

        pull_type = content.get("pull_type", 0)
        # 设置额外参数pull_type
        ex_params["pull_type"] = pull_type

        # 参数检查
        for k in [date_interval, statistic_ids, server_ids]:
            if k:
                continue
            _e = f"date_interval:{date_interval}, statistic_ids{statistic_ids}, server_ids{server_ids}"
            logging.info("[ERROR] <DispatchRule> __make_content_info, params %s", _e)
            return None

        info_obj = {
            "schedule_name": schedule_name,  # 计划任务名
            "queue_name": queue_name,  # 任务队列名
            "appoint_server_ids": server_ids,  # 指定服务器id
            "server_id_slice_size": server_id_slice_size,  # 分服统计服务器切片大小
            "statistic_ids": statistic_ids,  # 统计id
            "statistic_ids_slice_size": statistic_ids_slice_size,  # 统计id切片大小
            "date_interval": date_interval,  # 日期区间:[{'sdate':'2017-01-01 00:00:00', 'edate':'2017-01-01 23:59:59'},]
            "pull_type": pull_type,  # 统计类型 见pull_types.py
            "ex_params": ex_params,  # 自定义参数
        }
        return info_obj

    # region 内部方法
    @staticmethod
    def __parse_date_interval(content):
        date_type = content.get("date_interval", "TODAY")
        date_appoint = content.get("date_appoint", None)
        if isinstance(date_appoint, list):
            # 指定日期
            if date_type == "SPLIT_DATE_BY_DAY":
                # 以天为单位分割日期
                return split_date_str_by_day(date_appoint[0], date_appoint[1])

            return [{"sdate": date_appoint[0], "edate": date_appoint[1]}]

        now = datetime.datetime.now()
        if date_type == "TODAY":
            # 今天至今
            # 0点的 sdate 处理为昨天
            fix_0 = now + datetime.timedelta(minutes=-1)
            sdate = datetime.datetime(fix_0.year, fix_0.month, fix_0.day, 00, 00, 00, 0)
            edate = now
        elif date_type == "START_OF_HOUR":
            # 当前小时
            # 01分处理为前一小时
            fix_0 = now + datetime.timedelta(minutes=-1)
            sdate = datetime.datetime(fix_0.year, fix_0.month, fix_0.day, fix_0.hour, 00, 00, 0)
            edate = datetime.datetime(fix_0.year, fix_0.month, fix_0.day, fix_0.hour, 59, 59, 0)
        elif date_type == "ACROSS_DAY":
            # 昨天一天的数据
            yesterday = now + datetime.timedelta(days=-1)
            sdate = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 00, 00, 00, 0)
            edate = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 0)
        elif date_type == "WEEK":
            # 昨天的周一至昨天的数据
            yesterday = now + datetime.timedelta(days=-1)
            week = yesterday.weekday()
            monday = yesterday + datetime.timedelta(days=-week)
            sdate = datetime.datetime(monday.year, monday.month, monday.day, 00, 00, 00, 0)
            edate = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 0)
        elif date_type == "MONTH":
            # 昨天的月初至昨天的数据
            yesterday = now + datetime.timedelta(days=-1)
            sdate = datetime.datetime(yesterday.year, yesterday.month, 1, 00, 00, 00, 0)
            edate = datetime.datetime(yesterday.year, yesterday.month, yesterday.day, 23, 59, 59, 0)
        else:
            return []

        return [
            {
                "sdate": sdate.strftime("%Y-%m-%d %H:%M:%S"),
                "edate": edate.strftime("%Y-%m-%d %H:%M:%S"),
            }
        ]

    def __parse_statistic_ids(self, content):
        statistic_ids = content.get("statistic_ids", [])
        statistic_ids_by_sql = content.get("statistic_ids_by_sql")
        if statistic_ids_by_sql:
            result_ids = self.sql_get_ids(statistic_ids_by_sql)
            if statistic_ids:
                statistic_ids.extend(result_ids)
            else:
                statistic_ids = result_ids
        if not statistic_ids:
            logging.info("[ERROR] <DispatchRuleStatisticTask> statistic_ids is None, content:%s", content)
            return []
        return statistic_ids

    def __parse_server_ids(self, content):
        # 获取server_ids
        appoint_server_ids = content.get("appoint_server_ids", None)
        server_ids_by_sql = content.get("appoint_server_ids_by_sql")
        if server_ids_by_sql:
            result_ids = self.sql_get_ids(server_ids_by_sql)
            if appoint_server_ids:
                appoint_server_ids.extend(result_ids)
            else:
                appoint_server_ids = result_ids
        if not appoint_server_ids:
            return []
        return appoint_server_ids

    @staticmethod
    def __auto_set_slice_size(p_info: dict):
        # 自动分片
        standard_server_slice = 100  # 标准服列表分片数
        standard_task_cnt = 200  # 标准task总个数
        standard_value = standard_server_slice * standard_task_cnt  # 标准值

        len_stats_ids = len(p_info["statistic_ids"])
        len_server_ids = len(p_info["appoint_server_ids"])
        cal_factor = len_server_ids * len_stats_ids / standard_value
        if cal_factor <= 1:
            p_info["server_id_slice_size"] = standard_server_slice
        else:
            p_info["server_id_slice_size"] = int(standard_server_slice * sqrt(cal_factor))

        p_info["statistic_ids_slice_size"] = 1  # 每个统计单独分片
        task_cnt = int(len_stats_ids * max(len_server_ids / p_info["server_id_slice_size"], 1))
        logging.info(
            "<__auto_split> len_stats_ids:%d, len_server_ids:%d, info.server_id_slice_size:%s, task_cnt:%d",
            len_stats_ids,
            len_server_ids,
            p_info["server_id_slice_size"],
            task_cnt,
        )

    def __split_content_info(self, info: dict):
        if info["server_id_slice_size"] is None:
            # 自动设置分片数
            self.__auto_set_slice_size(info)

        # 服务器列表切片
        server_id_group = split_list(info["appoint_server_ids"], info["server_id_slice_size"])

        # 统计id切片
        if info["statistic_ids_slice_size"] > 0:
            statistic_id_group = split_list(info["statistic_ids"], info["statistic_ids_slice_size"])
        else:
            statistic_id_group = [info["statistic_ids"]]

        # 切割param（服id、统计id）
        params_list = []
        for svr_id_list in server_id_group:
            # 服id切割
            for stat_id_list in statistic_id_group:
                # 统计id切割
                for date_p in info["date_interval"]:
                    # 日期切割
                    params = {
                        "statistic_id": stat_id_list,
                        "server_ids": svr_id_list,
                        "schedule_name": info["schedule_name"],
                        "ex_params": info["ex_params"],
                        "pull_type": info["pull_type"],
                    }
                    params_p = copy.copy(params)
                    params_p.update(date_p)
                    params_list.append(params_p)
        # 任务乱序
        random.shuffle(params_list)
        return params_list

    def get_all_server_ids(self, status=""):
        """
        :param status:
        :return:
        """
        # 根据status筛选服务器
        status_cond = "2, -1" if status == "all" else "2"
        sql = f"""
            SELECT id
            FROM svr_server
            WHERE is_pull = 1
            AND status IN ({status_cond})
            ORDER BY game_addr
        """

        return self.sql_get_ids(sql)

    @staticmethod
    def sql_get_ids(sql):
        """
        :param sql:
        :return:
        """
        api_pool = get_dbpool(app.conf.API_READ_MYSQL_CONFIG)
        result = MysqlOperation().get_all(sql, api_pool.get_connection())
        return [_v[0] for _v in result]

    # endregion


@rule_register(
    inst_name_list=[
        "pull_task_instance",
        "pull_collect_instance",
        "statistic_task_instance",
        "statistic_collect_instance",
    ]
)
class DispatchRuleStatisticTask(DispatchRuleStatisticTaskLogic):
    """
    DispatchRuleStatisticTask
    若直接将@rule_register装饰在DispatchRuleStatisticTaskLogic上会导致继承问题，所以单独继承注册处理
    """
