# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9
from yyxx_game_pkg.utils.decorator import singleton


# region 注册函数
def rule_register(*args, **kwargs):
    inst_name_list = kwargs.get("inst_name_list")
    if not inst_name_list:
        return

    def _deco(class_method):
        for inst_name in inst_name_list:
            obj = class_method()
            obj.inst_name = inst_name
            RuleManager().add_rule(inst_name, obj)

    return _deco


# endregion


@singleton
class RuleManager(object):
    def __init__(self):
        self.__rules = dict()

    # region property
    @property
    def rules(self):
        return self.__rules

    # endregion

    # region 外部方法
    def add_rule(self, key, val):
        self.__rules[key] = val

    # endregion
