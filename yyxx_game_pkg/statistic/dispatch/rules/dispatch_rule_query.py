# -*- coding: utf-8 -*-
"""
dispatch_rule_query
"""
import copy

from celery import current_app as app
from yyxx_game_pkg.helpers.redis_helper import get_redis
from yyxx_game_pkg.utils.xdate import split_date_str_by_day

from ..core.manager import rule_register
from .rule_base import ProtoSchedule, RuleBase


@rule_register(inst_name_list=["query_task_instance", "query_collect_instance"])
class DispatchRuleQuery(RuleBase):
    """
    query rule
    """

    def build(self, schedule: ProtoSchedule):
        param = {"schedule_name": schedule.schedule_name}
        param.update(schedule.schedule_content[0])
        sql_md5 = param.get("sql_md5")
        if not sql_md5:
            return None

        # 根据md5获取查询参数
        query_param = self.__get_sql_data(sql_md5)

        # 获取队列名
        queue_name = schedule.queue

        # 获取自定义查询参数dispatch params
        dispatch_params = query_param.get("dispatch_params")

        # 更新队列名
        queue_name = self.__update_queue_query_name(queue_name, dispatch_params, param)

        # 参数赋值
        param.update(query_param)

        # 构建查询参数列表
        param_list = self.__make_param_list(param, dispatch_params)

        # 构建signature
        sig = self.make_signature_group(
            app.conf.get("CUSTOM_TASK_REGISTER_PATH"),
            self.inst_name,
            queue_name,
            schedule.priority,
            kwargs_list=param_list,
        )
        return sig

    # region 内部方法
    def __get_sql_data(self, sql_md5):
        """
        从redis中获取完整的sql语句
        :param sql_md5:
        :return:
        """
        redis_handle = get_redis(app.conf.get("REDIS_CONFIG"))
        query_param = redis_handle.get_data(sql_md5)
        return eval(query_param)

    def __update_queue_query_name(self, queue_name, dispatch_params, param):
        # 队列名更新
        queue_query_name_base = (
            "queue_query" if queue_name is None else queue_name.split("#")[0]
        )
        alias = param.get("alias")
        if alias is not None:
            queue_name = f"{queue_query_name_base}#{alias}"

        # 自定义队列名
        if isinstance(dispatch_params, dict):
            custom_query_name = dispatch_params.get("query_name")
            if custom_query_name is not None:
                queue_name = queue_name.replace(
                    queue_query_name_base, custom_query_name
                )

        return queue_name

    def __make_param_list(self, param, dispatch_params):
        if (
            not isinstance(dispatch_params, dict)
            or param.get("schedule_name") == "work_template_query_collect"
        ):
            return [param]
        date_split_slice = dispatch_params.get("date_split_slice")
        if date_split_slice is None:
            return [param]

        sdate_str = param["sdate"][0]
        edate_str = param["edate"][0]
        date_list = split_date_str_by_day(sdate_str, edate_str, int(date_split_slice))

        param_list = []
        for date_interval in date_list:
            param_p = copy.deepcopy(param)
            param_p["sdate"][0] = date_interval["sdate"]
            param_p["edate"][0] = date_interval["edate"]
            param_list.append(param_p)

        return param_list

    # endregion
