import re
import time

import yaml

from common.logger import logger
from src.common.common import PrettyDict


def load_yaml(file) -> dict:
    """加载yaml文件

    :param file: yaml文件
    :return: 解析后的json格式数据
    """
    parse_yaml = dict()
    try:
        with open(file, 'r', encoding='utf-8') as f:
            parse_yaml = yaml.safe_load(f)
    except IOError as ioe:
        logger.exception(ioe)
    except yaml.YAMLError as ye:
        logger.exception(ye)
    finally:
        if f:
            f.close()
    return parse_yaml


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


def to_dict(string: str, separator: str = ";", pair_symbol: str = "=") -> dict:
    if not string:
        return dict()
    pair_list = string.split(separator)
    return dict(map(lambda s: tuple(s.split(pair_symbol, maxsplit=1)), pair_list))


def trans_dict(dikt: dict) -> dict | PrettyDict:
    """
    将字典转换成特殊对象, 既能使用字典取值方式, 又能使用对象取值方式

    :param dikt: 待转换的字典
    :return: 转换后的对象obj
    """
    if not isinstance(dikt, dict):
        return dikt
    d = PrettyDict()
    for k, v in dikt.items():
        d[k] = trans_dict(v)
    return d


def recover_dict(dikt: dict) -> dict:
    """
    将转换的特殊字典对象还原

    :param dikt: 转换后的特殊字典对象
    :return: dict
    """
    if not isinstance(dikt, dict):
        return dikt
    d = dict()
    for k, v in dikt.items():
        d[k] = recover_dict(v)
    return d


if __name__ == "__main__":
    st = 'inline; filename="1000g0cg2juvge7aj40005ndt84t0965fu86faoo"; filename*=utf-8''1000g0cg2juvge7aj40005ndt84t0965fu86faoo'
    print(re.search('(?<=filename=").*(?=")', st).group())
