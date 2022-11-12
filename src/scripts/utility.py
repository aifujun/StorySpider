# Author: aifujun
# Project: GetNovel
# File: scripts/utility.py
# Date: 2022-03-16 21:11
# Note:
import time


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
    a = [(1,2), (90, 8)]
    for i, m in enumerate(a):
        print(i, m)
    print(get_time())
