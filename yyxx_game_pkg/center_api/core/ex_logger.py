# -*- coding: utf-8 -*-
import logging
import logging.handlers
import socket
import time
from yyxx_game_pkg.conf import settings
from yyxx_game_pkg.xtrace.helper import get_current_trace_id


# log记录-块
class Logger(object):

    __log_dict = dict()

    @staticmethod
    def get_logger(log_name=settings.ERROR_LOG_NAME):
        now_day = time.strftime("%Y-%m-%d", time.localtime())
        log_name = "{}_{}_{}".format(log_name, now_day, socket.gethostname())
        __logger = Logger.__log_dict.get(log_name)

        trace_id = get_current_trace_id()[2:]
        trace_format = logging.Formatter(f'%(asctime)s [%(levelname)s] ["trace":"{trace_id}"] %(message)s')

        if not __logger:
            __logger = logging.getLogger(log_name)
            __logger.setLevel(level=logging.INFO)
            __path_file_name = "{}{}.log".format(settings.LOG_DIR, log_name)
            __file_handler = logging.FileHandler(filename=__path_file_name)
            __file_handler.setFormatter(trace_format)
            __logger.addHandler(__file_handler)
            Logger.__log_dict[log_name] = __logger
            # Create new logger
            log_str = f'info:({log_name} new logger has been created) param:({Logger.__log_dict})'
            __logger.info(log_str)
        else:
            try:
                __logger.handlers[0].setFormatter(trace_format)
            except Exception as e:
                print(e)
        return __logger
