# Author: aifujun
# Project: GetNovel
# File: common/logger.py
# Date: 2022-03-16 21:03
# Note:

import re
import logging
import threading

from common.constants import LOG_FILE


class SingletonType(type):
    _instance_lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            with SingletonType._instance_lock:
                if not hasattr(cls, "_instance"):
                    cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
        return cls._instance


class CrlfFormatter(logging.Formatter):
    def formatMessage(self, record):
        # 过滤message中的\r\n\b
        message = super(CrlfFormatter, self).formatMessage(record)
        message = re.sub('[\r\n\b]', ' ', message)
        return message


class Logger(metaclass=SingletonType):
    logger = logging.getLogger('logger.root')

    def __init__(self) -> None:
        # 如果这个属性为True，记录到这个记录器的事件除了会发送到此记录器的所有处理程序外，
        # 还会传递给更高级别（祖先）记录器的处理器，此外任何关联到这个记录器的处理器。
        # 消息会直接传递给祖先记录器的处理器 —— 不考虑祖先记录器的级别和过滤器。
        # 如果为False，记录消息将不会传递给当前记录器的祖先记录器的处理器。
        # 默认值为True
        self.logger.propagate = True
        self.logger.isEnabledFor(logging.INFO)
        self.logger.setLevel(logging.INFO)

        self.standard_formatter = "[%(asctime)s][%(levelname)s][%(name)s][%(process)d][%(threadName)s][%(thread)d]" \
                                  "[%(filename)s][%(funcName)s][%(lineno)s]%(message)s"
        self.formatter_str = CrlfFormatter(self.standard_formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(self.formatter_str)
        self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setFormatter(self.formatter_str)
        self.logger.addHandler(file_handler)

    @classmethod
    def set_level(cls, level):
        cls.logger.setLevel(level)


logger = Logger().logger


if __name__ == '__main__':
    logger.debug('this is a debug log...')
    logger.info('this is a info log...')
    logger.error('this is an error log...')
