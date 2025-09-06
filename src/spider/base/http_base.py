import random

import requests

from common.error.error_code import HttpStatusCode
from common.error.exceptions import HttpCodeException
from common.logger import logger
from common.utils.decorator import retry


class RequestBase(object):
    def __init__(self, referer: str = None, token: str = None, cookies: str = None, proxies: list = None):
        self.headers = {
            'Referer': referer,
            'X-token': token,
            'Cookie': cookies,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0"
        }
        self.proxies = random.choice(proxies) if proxies else proxies

    @retry()
    def head(self, url: str, **kwargs):
        """
        HEAD：请求页面的首部

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        kwargs.setdefault("allow_redirects", True)
        response = requests.head(url, headers=self.headers, proxies=self.proxies, **kwargs)
        if response.status_code != HttpStatusCode.OK.value:
            logger.error(f"Get url: <{url}>, params: {kwargs.get('params')} failed, errorCode: {response.status_code}.")
            raise HttpCodeException(code=response.status_code)
        logger.info(f"Get url: <{url}> html page successful.")
        return response

    @retry()
    def get(self, url: str, **kwargs):
        """
        GET：请求指定的页面信息，并返回实体主体

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        response = requests.get(url, headers=self.headers, proxies=self.proxies, **kwargs)
        if response.status_code != HttpStatusCode.OK.value:
            logger.error(f"Get url: <{url}>, params: {kwargs.get('params')} failed, errorCode: {response.status_code}.")
            raise HttpCodeException(code=response.status_code)
        logger.info(f"Get url: <{url}> html page successful.")
        return response

    @retry()
    def post(self, url: str, **kwargs):
        """
        POST：在服务器新建一个资源

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        response = requests.post(url, headers=self.headers, proxies=self.proxies, **kwargs)
        pass

    @retry()
    def put(self, url: str, **kwargs):
        """
        PUT：在服务器更新资源（客户端提供改变后的完整资源

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        response = requests.put(url, headers=self.headers, proxies=self.proxies, **kwargs)
        pass

    @retry()
    def patch(self, url: str, **kwargs):
        """
        PATCH：在服务器更新资源（客户端只提供改变了属性）

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        response = requests.patch(url, headers=self.headers, proxies=self.proxies, **kwargs)
        pass

    @retry()
    def delete(self, url: str, **kwargs):
        """
        DELETE：从服务器删除资源

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        response = requests.delete(url, headers=self.headers, proxies=self.proxies, **kwargs)
        pass

    @retry()
    def options(self, url: str, **kwargs):
        """
        OPTIONS：用于获取目的资源所支持的通信选项

        :param url: 访问的url
        :param kwargs:
            params: Any = ...,
            data: Any | None = ...,
            headers: Any | None = ...,
            cookies: Any | None = ...,
            files: Any | None = ...,
            auth: Any | None = ...,
            timeout: Any | None = ...,
            allow_redirects: bool = ...,
            proxies: Any | None = ...,
            hooks: Any | None = ...,
            stream: Any | None = ...,
            verify: Any | None = ...,
            cert: Any | None = ...,
            json: Any | None = ...
        """
        response = requests.options(url, headers=self.headers, proxies=self.proxies, **kwargs)
        pass


if __name__ == "__main__":
    u = "https://v.douyin.com/iMmkban/"
    hp = RequestBase().head(u)
    print(hp.url)

