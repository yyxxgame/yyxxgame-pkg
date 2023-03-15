# -*- coding: utf-8 -*-
# @Author   : KaiShin
# @Time     : 2023/3/14

from yyxx_game_pkg.logger import log
from yyxx_game_pkg.xtrace.helper import get_current_trace_id

logger = log.Log()


def local_log(msg):
    """
    local log rotate file
    :param msg:
    :return:
    """
    trace_id = get_current_trace_id()
    msg = f"[{trace_id}] {msg}"
    logger.local_log(msg)
