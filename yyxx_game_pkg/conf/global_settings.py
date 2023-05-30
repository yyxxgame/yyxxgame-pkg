# -*- coding: utf-8 -*-
# @Author   : pmz
# @Time     : 2023/05/05 09:57:27
# @Software : python3.11
# @Desc     : global_settings

# DEBUG
DEBUG = False

# ----------------------------------------------------------------
TIME_ZONE = "Asia/Shanghai"
LANGUAGE_CODE = "zh-hans"
DEFAULT_CHARSET = "utf-8"

# DB settings
DATABASES = {}
REDIS_SERVER = {}

# Project key
# 客户端加密key
API_KEY = ""
# 服务端加密key
SERVER_KEY = ""
# 单服接口加密key
SERVER_API_KEY = ""
# 接口数据加密key
ENCRYPTION_KEY = ""

# 接口日志
ERROR_LOG_NAME = "python_center_api_error"
PARAM_LOG_NAME = "python_center_api_param"
LOG_DIR = "/opt/log/python/"

# 服务器配置
SERVER_IP = "127.0.0.1"
IS_TEST = True

# endregion
Dummy = None

# DATE  DATETIME format
DATE_INPUT_FORMATS = [
    "%Y-%m-%d",  # '2006-10-25'
    "%m/%d/%Y",  # '10/25/2006'
    "%m/%d/%y",  # '10/25/06'
    "%b %d %Y",  # 'Oct 25 2006'
    "%b %d, %Y",  # 'Oct 25, 2006'
    "%d %b %Y",  # '25 Oct 2006'
    "%d %b, %Y",  # '25 Oct, 2006'
    "%B %d %Y",  # 'October 25 2006'
    "%B %d, %Y",  # 'October 25, 2006'
    "%d %B %Y",  # '25 October 2006'
    "%d %B, %Y",  # '25 October, 2006'
]

TIME_INPUT_FORMATS = [
    "%H:%M:%S",  # '14:30:59'
    "%H:%M:%S.%f",  # '14:30:59.000200'
    "%H:%M",  # '14:30'
]

DATETIME_INPUT_FORMATS = [
    "%Y-%m-%d %H:%M:%S",  # '2006-10-25 14:30:59'
    "%Y-%m-%d %H:%M:%S.%f",  # '2006-10-25 14:30:59.000200'
    "%Y-%m-%d %H:%M",  # '2006-10-25 14:30'
    "%m/%d/%Y %H:%M:%S",  # '10/25/2006 14:30:59'
    "%m/%d/%Y %H:%M:%S.%f",  # '10/25/2006 14:30:59.000200'
    "%m/%d/%Y %H:%M",  # '10/25/2006 14:30'
    "%m/%d/%y %H:%M:%S",  # '10/25/06 14:30:59'
    "%m/%d/%y %H:%M:%S.%f",  # '10/25/06 14:30:59.000200'
    "%m/%d/%y %H:%M",  # '10/25/06 14:30'
]

# First day of week, to be used on calendars
# 0 means Sunday, 1 means Monday...
FIRST_DAY_OF_WEEK = 0

###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = "logging.config.dictConfig"

# Custom logging configuration.
LOGGING = {}
