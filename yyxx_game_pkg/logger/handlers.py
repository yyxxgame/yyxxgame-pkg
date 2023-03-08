# -*- coding: utf-8 -*-
"""
@File: handlers.py
@Author: ltw
@Time: 2022/6/22
"""
import os
import time
import fcntl
import traceback
import logging.handlers


class MultiProcessTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    自定义多进程下TimedRotatingFileHandler
    """

    def rollover_at(self):
        """
        计算下次滚动时间
        """
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        new_rollover_at = self.computeRollover(current_time)
        while new_rollover_at <= current_time:
            new_rollover_at = new_rollover_at + self.interval
        # If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == "MIDNIGHT" or self.when.startswith("W")) and not self.utc:
            dst_at_rollover = time.localtime(new_rollover_at)[-1]
            if dst_now != dst_at_rollover:
                if (
                    not dst_now
                ):  # DST kicks in before next rollover, so we need to deduct an hour
                    addend = -3600
                else:  # DST bows out before next rollover, so we need to add an hour
                    addend = 3600
                dst_at_rollover += addend
        self.rolloverAt = new_rollover_at

    def doRollover(self):
        """
        do a rollover; in this case, a date/time stamp is appended to the filename
        when the rollover happens.  However, you want the file to be named for the
        start of the interval, not the current time.  If there is a backup count,
        then we have to get a list of matching filenames, sort them and remove
        the one with the oldest suffix.
        """

        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started at and make it a TimeTuple
        current_time = int(time.time())
        dst_now = time.localtime(current_time)[-1]
        diff_t = self.rolloverAt - self.interval
        if self.utc:
            time_tuple = time.gmtime(diff_t)
        else:
            time_tuple = time.localtime(diff_t)
            dst_then = time_tuple[-1]
            if dst_now != dst_then:
                if dst_now:
                    addend = 3600
                else:
                    addend = -3600
                time_tuple = time.localtime(diff_t + addend)
        dfn = self.baseFilename + "." + time.strftime(self.suffix, time_tuple)
        if os.path.exists(dfn):
            self.rollover_at()
            return
        # Issue 18940: A file may not have been created if delay is True.
        if not os.path.exists(dfn) and os.path.exists(self.baseFilename):
            # lock rename file
            try:
                with open(self.baseFilename, "a", encoding="utf-8") as file:
                    # LOCK_EX 独占
                    # LOCK_NB 非阻塞式
                    fcntl.flock(file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)  # 获取文件锁
                    os.rename(self.baseFilename, dfn)  # 更改文件名
                    fcntl.flock(file.fileno(), fcntl.LOCK_UN)  # 释放文件锁
            except IOError:
                traceback.print_exc()
                return

        if self.backupCount > 0:
            for _d in self.getFilesToDelete():
                os.remove(_d)
        if not self.delay:
            self.stream = self._open()
        self.rollover_at()
