import ctypes
import threading
import time

from functools import wraps

from src.common.error.exceptions import WindowsAPIException
from src.common.logger import logger


class Singleton(object):
    """
    单例模式装饰器, 双重检查加锁提高效率(只有在第一次执行此方法时，才需要进程锁进行同步)
    """
    _instance_lock = threading.Lock()

    def __init__(self, cls):
        self._cls = cls
        self._instance = None

    def __call__(self):
        if self._instance is None:
            with self._instance_lock:
                if self._instance is None:
                    self._instance = self._cls()
        return self._instance


def checked(func):
    """ctypes函数执行状态检查，类方法装饰器"""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            ret = func(self, *args, **kwargs)
            if not ret and ctypes.get_errno():
                raise WindowsAPIException("Error calling " + func.__name__)
            return ret
        except Exception:
            raise WindowsAPIException(f"Error calling {func.__name__}, error: {ctypes.get_errno()}")
    return wrapper


def retry(retry_count: int = 5, interval: int = 3):
    """BaseException重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for retry_time in range(retry_count):
                try:
                    res = func(*args, **kwargs)
                    return res
                except BaseException as e:
                    logger.warning(f'Run function: {func.__name__} error, retry: {retry_time}, except: {e}')
                    if retry_time == retry_count:
                        raise
                    time.sleep(interval)
        return wrapper
    return decorator
