# -*- coding: utf-8 -*-
"""
@File: pull_types
@Author: ltw
@Time: 2022/7/27
"""
# 同步dispatch_server的pull_types配置
# 任务拉取类型
# 需同步到dispatch
PULL_TYPE_FULL = 0  # before_process -> process -> after_process
PULL_TYPE_BEFORE = 1  # before_process
PULL_TYPE_PROCESS = 2  # process
PULL_TYPE_AFTER = 3  # after_process
