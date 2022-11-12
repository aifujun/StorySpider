
import random

import requests
from lxml import etree

from common.errCode import StatusCode
from common.logger import logger


class Spider(object):
    def __init__(self, referer: str = '', token: str = '', cookie: str = '', proxies: list = None):
        if proxies is None:
            proxies = []
        self.headers = {
            'Referer': referer,
            'X-token': token,
            'Cookie': cookie,
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:23.0) Gecko/20131011 Firefox/23.0"
        }
        self.proxies = proxies

    def get_html(self, url: str, timeout: int = 120):
        """
        获取当前章节页面信息

        Args:
            url: 访问的url
            timeout: 访问超时时间(s)
        Return:
            经etree.HTML转换后的数据
        """
        html = None
        self.proxies = random.choice(self.proxies) if self.proxies else self.proxies
        response = requests.get(url, headers=self.headers, timeout=timeout, proxies=self.proxies)
        if response.status_code != StatusCode.OK.value:
            logger.error(f"get html page failed, errorCode: {response.status_code}")
            return response.status_code, html
        response.encoding = response.apparent_encoding
        html = etree.HTML(response.text)
        logger.info("get html page successful")
        return response.status_code, html


if __name__ == '__main__':
    print(Spider().get_html('https://www.baidu.com'))
