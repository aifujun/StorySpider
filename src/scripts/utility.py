
import time

from functools import wraps

from common.exception import HttpCodeException


def retry(retry_count: int = 5, interval: int = 1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retry_count):
                try:
                    res = func(*args, **kwargs)
                    return res
                except HttpCodeException:
                    time.sleep(interval)
                    continue
            return None
        return wrapper
    return decorator


def get_time():
    """获取当前时间"""
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return localtime


def get_headers():
    """
    获取构造一个请求头

    Returns:

    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49 QIHU 360SE',
        'Cookie': '',
    }
    return headers


if __name__ == '__main__':
    a = [(1, 2), (90, 8)]

