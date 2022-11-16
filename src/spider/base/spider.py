
import random

import requests
from lxml import etree

from common.errCode import HttpStatusCode
from common.exception import HttpCodeException
from common.logger import logger
from scripts.utility import retry


class Spider(object):
    def __init__(self, referer: str = None, token: str = None, cookie: str = None, proxies: list = None):
        self.headers = {
            'Referer': referer,
            'X-token': token,
            'Cookie': cookie,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0"
        }
        self.proxies = random.choice(proxies) if proxies else proxies

    @retry()
    def get_html(self, url: str, timeout: int = 180):
        """
        获取当前章节页面信息

        Args:
            url: 访问的url
            timeout: 访问超时时间(s)
        Return:
            经etree.HTML转换后的数据
        """
        response = requests.get(url, headers=self.headers, timeout=timeout, proxies=self.proxies)
        if response.status_code != HttpStatusCode.OK.value:
            logger.error(f"Get url: <{url}> html page failed, errorCode: {response.status_code}.")
            raise HttpCodeException
        response.encoding = response.apparent_encoding
        html_tree = etree.HTML(response.text)
        logger.info(f"Get url: <{url}> html page successful.")
        return html_tree

    def get_book_info(self, *args, **kwargs) -> None: ...

    def get_chapter(self, *args, **kwargs) -> None: ...


if __name__ == '__main__':
    print(Spider().get_html('https://www.baidu.com'))
