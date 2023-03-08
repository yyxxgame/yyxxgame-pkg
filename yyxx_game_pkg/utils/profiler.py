# # -*- coding: utf-8 -*-
"""
性能分析器
"""
import io
import time
import cProfile
from functools import wraps
from line_profiler import LineProfiler


class Profiler:
    """
    Profiler
    """

    def __init__(self):
        self.__lp = LineProfiler()

    def execute(self, main_func_inst, *args, assist_func_list=None, **kwargs):
        """
        执行分析
        :param main_func_inst: 主函数入口
        :param assist_func_list: 子函数列表
        :param args:
        :param kwargs:
        :return:
        """
        if assist_func_list is not None:
            for func in assist_func_list:
                self.__lp.add_function(func)
        lp_wrapper = self.__lp(main_func_inst)
        lp_wrapper(*args, **kwargs)
        self.__lp.print_stats()


def func_time(func):
    """
    简单记录执行时间
    :param func:
    :return:
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(func.__name__, args, kwargs, 'took', end - start, 'seconds')
        return result

    return wrapper


def func_cprofile(func):
    """
    内建分析器
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        profile = cProfile.Profile()
        try:
            profile.enable()
            result = func(*args, **kwargs)
            profile.disable()
            return result
        finally:
            profile.print_stats(sort='time')

    return wrapper


def func_line_time(follow=()):
    """
    每行代码执行时间详细报告
    :param follow: 内部调用方法
    :return:
    """
    def decorate(func):
        @wraps(func)
        def profiled_func(*args, **kwargs):
            profiler = LineProfiler()
            try:
                profiler.add_function(func)
                for _f in follow:
                    profiler.add_function(_f)
                profiler.enable_by_count()
                return func(*args, **kwargs)
            finally:
                _s = io.StringIO()
                profiler.print_stats(stream=_s)
                print(f"<line_profiler> {_s.getvalue()}")

        return profiled_func

    return decorate


"""
# example

def do_stuff(numbers):
    do_other_stuff(numbers)
    s = sum(numbers)
    l = [numbers[i]/43 for i in range(len(numbers))]
    m = ['hello'+str(numbers[i]) for i in range(len(numbers))]


@func_line_time()
def do_other_stuff(numbers):
    s = sum(numbers)


def main_instance():
    import random
    numbers = [random.randint(1, 100) for i in range(1000)]
    do_stuff(numbers)
    do_other_stuff(numbers)


if __name__ == '__main__':
    main_instance()
    
    # profile = Profiler()
    # profile.execute(main_func_inst=main_instance, assist_func_list=[do_stuff, do_other_stuff])
    
"""
