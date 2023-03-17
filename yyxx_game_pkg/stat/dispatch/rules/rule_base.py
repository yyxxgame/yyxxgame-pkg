# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/13
from yyxx_game_pkg.stat.dispatch.core.structs import ProtoSchedule


class RuleBase(object):
    def __init__(self):
        self._business_instance_name = None

    # region property
    @property
    def inst_name(self):
        return self._business_instance_name

    @inst_name.setter
    def inst_name(self, val):
        self._business_instance_name = val

    # endregion

    # region 继承方法
    def build(self, schedule: ProtoSchedule):
        """
        构建独立的分发任务标签
        :return: [group, chord, chain, signature]
        """
        pass
        return None

    # endregion
