# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/9
"""
rule decorator
"""
from yyxx_game_pkg.utils.decorator import singleton


# region 注册函数
def rule_register(*_, **kwargs):
    """
    注册函数
    :param _:
    :param kwargs:
    :return:
    """
    inst_name_list = kwargs.get("inst_name_list")
    if not inst_name_list:
        return None

    def _deco(class_method):
        for inst_name in inst_name_list:
            obj = class_method()
            obj.inst_name = inst_name
            RuleManager().add_rule(inst_name, obj)

    return _deco


# endregion


@singleton
class RuleManager:
    """
    RuleManager
    """

    def __init__(self):
        self.__rules = {}

    # region property
    @property
    def rules(self):
        """
        :return:
        """
        return self.__rules

    # endregion

    # region 外部方法
    def add_rule(self, key, val):
        """
        :param key:
        :param val:
        :return:
        """
        self.__rules[key] = val

    # endregion
