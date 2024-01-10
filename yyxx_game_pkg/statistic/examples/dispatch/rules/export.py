# -*- coding: utf-8 -*-
"""
@File: export
@Author: ltw
@Time: 2024/1/5
"""
import importlib
import logging
import pathlib

LOAD_MODULE_PATHS = ("rules",)


def auto_import(load_paths=LOAD_MODULE_PATHS):
    """
    自动 import 本地 rules
    :param load_paths:
    :return:
    """
    # 手动 import 公共 rules
    from yyxx_game_pkg.statistic.dispatch.rules import (
        dispatch_rule_multi_workflow,
        dispatch_rule_query,
        dispatch_rule_statistic_task,
        dispatch_rule_workflow,
    )

    for load_path in load_paths:
        for file_path in pathlib.Path().joinpath(load_path).iterdir():
            if file_path.is_dir():
                continue
            if file_path.name.startswith("__init__"):
                continue
            if file_path.name.startswith("export.py"):
                continue
            if not file_path.name.endswith(".py"):
                continue
            import_path = str(file_path).replace("/", ".")[:-3]
            module = importlib.import_module(import_path)
            logging.info("******** auto import local %s", module)
