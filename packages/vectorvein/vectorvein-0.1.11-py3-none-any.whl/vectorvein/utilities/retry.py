# @Author: Bi Ying
# @Date:   2024-08-14 13:03:10
import time


class Retry:
    def __init__(self, function):
        self.function = function
        self.__retry_times = 3
        self.__sleep_time = 1
        self.pargs = []
        self.kwargs = {}

    def args(self, *args, **kwargs):
        self.pargs = args
        self.kwargs = kwargs
        return self

    def retry_times(self, retry_times: int):
        self.__retry_times = retry_times
        return self

    def sleep_time(self, sleep_time):
        self.__sleep_time = sleep_time
        return self

    def run(self):
        try_times = 0
        while try_times < self.__retry_times:
            try:
                return True, self.function(*self.pargs, **self.kwargs)
            except Exception as e:
                print(f"{self.function.__name__} 函数出错：{e}")
                try_times += 1
                time.sleep(self.__sleep_time)
        return False, None
