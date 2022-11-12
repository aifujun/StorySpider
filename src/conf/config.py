# Author: aifujun
# Project: GetNovel
# File: conf/config.py
# Date: 2022-03-16 21:04
# Note:

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class LogConfig(object):
    LOGFILE_DIR = os.path.join(BASE_DIR, "log")
    LOGS_FILENAME = os.path.join(BASE_DIR, "log", "logs.log")
    DEBUG_FILENAME = os.path.join(BASE_DIR, "log", "debug.log")

    DETAILED_FORMAT = '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s]' \
                      '[%(filename)s:%(lineno)d][%(levelname)s]%(message)s'
    STANDARD_FORMAT = '[%(asctime)s][%(filename)s:%(lineno)d][%(levelname)s]%(message)s'
    SIMPLE_FORMAT = '[%(asctime)s][%(levelname)s]%(message)s'

    CONSOLE_LEVEL = "DEBUG"
    DEBUG_LEVEL = "DEBUG"
    FILE_LEVEL = "INFO"


class Xpath(object):
    title = ''
    chapter = ''


if __name__ == '__main__':
    print(BASE_DIR)
