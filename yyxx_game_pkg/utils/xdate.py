# -*- coding: utf-8 -*-
"""
@File: xdate
@Author: ltw
@Time: 2022/8/4
"""
import re
import time
import datetime
from enum import Enum

DAY = 1
WEEK = 2
MONTH = 3


# 时间转换
def str2date(date_str):
    """
    时间字符串转datetime obj
    """
    if isinstance(date_str, bytes):
        date_str = date_str.decode(encoding="utf8")

    if isinstance(date_str, (int, float)) or date_str.isnumeric():
        # 时间戳
        if len(str(date_str)) == 8:
            # 20230101
            return datetime.datetime.strptime(str(date_str), "%Y%m%d")
        # 1672502400 or 1672502400000
        return datetime.datetime.fromtimestamp(date_str)
    if len(date_str) == 19:
        # 常用时间格式 2023-01-01 00:00:00
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    iso_regex = (
        r"^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}(\.\d{1,6})?([+-]\d{2}:\d{2})?$"
    )
    if re.match(iso_regex, date_str.replace("Z", "+00:00")):
        # 符合iso格式的时间字符串 2022-03-08T16:30:00.000Z or 2023-03-08T20:45:17+08:00
        return datetime.datetime.fromisoformat(date_str)
    millisecond_regex = r".*(\.\d{1,6})$"
    if re.match(millisecond_regex, date_str):
        # 带毫秒的时间
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
    # 常用时间格式 2023-01-01
    return datetime.datetime.strptime(date_str, "%Y-%m-%d")


def str2date_str(date_str, fmt="%Y-%m-%d %H:%M:%S"):
    """
    将时间字符串转成另外格式的时间字符串
    """
    return str2date(date_str).strftime(fmt)


def str2day(date_str):
    """
    "2021-05-31 12:23:40" to YYYYMMDD
    """
    return datetime.datetime.strptime(date_str, "%Y%m%d")


def date2dt_day(date, _h=0, _m=0, _s=0):
    """
    "2021-05-31 12:23:40" to "2021-05-31 00:00:00"
    :param date: datetime obj
    :param _h: hour
    :param _m: minute
    :param _s: second
    :return: datetime obj
    """
    return datetime.datetime(date.year, date.month, date.day, int(_h), int(_m), int(_s))


def date2dt_day_end(date) -> datetime.datetime:
    """
    "2021-05-31 12:23:40" to "2021-05-31 23:59:59"
    :param date: datetime obj
    :return: datetime obj
    """
    return date2dt_day(date, 23, 59, 59)


def day2date(day, fmt="%Y%m%d") -> datetime.datetime:
    """
    "20210531" to "2021-05-31 00:00:00"
    :param day: 时间字符串
    :param fmt: 时间字符串格式 默认 "%Y%m%d"
    :return: datetime obj
    """
    return datetime.datetime.strptime(str(day), fmt)


def date2day(date):
    """
    "2021-05-31 12:23:40" to "20210531"
    """
    return date.strftime("%Y%m%d")


def day_diff(day1, day2):
    """
    day_diff(20210531, 20210529) -> 2
    """
    return (day2date(day2) - day2date(day1)).days


# 根据date获取第delta天时间
def delta_dt_day(date, delta=0, end=0):
    """
    :param date: 起始时间
    :param delta: 第几天
    :param end: 0: 00:00:00 / 1: 23:59:59
    :return:
    """
    if end:
        return date2dt_day_end(date) + datetime.timedelta(days=delta)
    return date2dt_day(date) + datetime.timedelta(days=delta)


def date2stamp(dt_date):
    """
    datetime转时间戳
    """
    return time.mktime(dt_date.timetuple())


def stamp2str(t_stamp, fmt="%Y-%m-%d %H:%M:%S"):
    """
    时间戳转日期字符串
    :param t_stamp: 时间戳
    :param fmt: 生成时间字符串格式 默认 %Y-%m-%d %H:%M:%S
    :return: 时间字符串
    """
    if not t_stamp:
        return ""
    time_array = time.localtime(t_stamp)
    return time.strftime(fmt, time_array)


def get_week_str(date, fmt="%Y%m%d"):
    """
    当前周 开始结束时间段
    get_week_str("2023-03-09 11:15:20") -> "2023-03-05~2023-03-11"
    :param date: 时间字符串
    :param fmt: 时间字符串格式 默认 "%Y%m%d"
    :return: 周期字符串
    """
    sdate = datetime.datetime.strptime(str(date), fmt)
    _, _, s_week_day = sdate.isocalendar()
    sday = (sdate - datetime.timedelta(days=s_week_day - 1)).strftime("%Y-%m-%d")
    eday = (sdate - datetime.timedelta(days=s_week_day - 7)).strftime("%Y-%m-%d")
    return f"{sday}~{eday}"


def date_type_trans(date, date_type=DAY, fmt="%Y%m%d"):
    """
    周期时间格式化
    :param date: 时间字符串
    :param date_type: 周期类型(1: 天 2: 周 3: 月)
    :param fmt: 时间字符串格式 默认 "%Y%m%d"
    :return: 周期字符串
    """
    if date_type == DAY:
        return datetime.datetime.strptime(str(date), fmt).strftime("%Y-%m-%d")
    if date_type == WEEK:
        return get_week_str(date, fmt)
    if date_type == MONTH:
        return datetime.datetime.strptime(str(date), fmt).strftime("%Y年%m月")
    return date


def to_start_of_interval(_t: datetime.datetime, unit="minute", interval=5):
    """
    to_start_of_interval("2023-03-09 11:16:20", 'minute', interval=5) -> datetime(2023-03-09 11:15:00)
    to_start_of_interval("2023-03-09 11:16:20", 'hour', interval=1) -> datetime(2023-03-09 11:00:00)
    """
    if unit == "minute":
        fix = _t.minute - _t.minute % interval
        _t = _t.replace(minute=fix, second=0, microsecond=0)
    elif unit == "hour":
        fix = _t.hour - _t.hour % interval
        _t = _t.replace(hour=fix, minute=0, second=0, microsecond=0)
    return _t


def split_date_str_by_day(sdate_str, edate_str, day_slice=1):
    """
    split_date_str_by_day
    """
    res_list = []
    if not sdate_str or not edate_str:
        return res_list

    # 按时间分配(天数)
    interval = datetime.timedelta(days=day_slice)
    start_dt = datetime.datetime.strptime(sdate_str, "%Y-%m-%d %H:%M:%S")
    edate_str = edate_str.replace("00:00:00", "23:59:59")
    end_dt = datetime.datetime.strptime(edate_str, "%Y-%m-%d %H:%M:%S")
    offset = datetime.timedelta(seconds=1)
    while start_dt < end_dt:
        next_dt = min((start_dt + interval - offset), end_dt)
        res_list.append(
            {
                "sdate": start_dt.strftime("%Y-%m-%d %H:%M:%S"),
                "edate": next_dt.strftime("%Y-%m-%d %H:%M:%S"),
            }
        )
        start_dt = next_dt + offset

    return res_list
