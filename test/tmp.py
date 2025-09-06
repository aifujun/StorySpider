import json
import os
import re
from urllib import parse
from urllib.parse import urlparse

import requests

from common.regular_expression import RegExpression
from conf.config import DYApiConfig

url = "https://www.douyin.com/aweme/v1/web/aweme/post/?sec_user_id=MS4wLjABAAAAw-MmWNqSSDu5O-sukdHy78GCEmxybtGoM87OOs7fuvE&count=10&max_cursor=0&aid=6383"

headers = {
    "Cookie": "msToken=uTa38b9QFHB6JtEDzH9S4np17qxpG6OrROHQ8at2cBpoKfUb0UWmTkjCSpf72EcUrJgWTIoN6UgAv5BTXtCbOAhJcIRKyZIT7TMYapeOSpf;odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; ttwid=1%7CWBuxH_bhbuTENNtACXoesI5QHV2Dt9-vkMGVHSRRbgY%7C1677118712%7C1d87ba1ea2cdf05d80204aea2e1036451dae638e7765b8a4d59d87fa05dd39ff; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVKUDZzbjNLRlFBNUROSEcyK2F4bXAwNG5cclxud1hBSTZDU1IyZW1sVUE5QTZ4aGQzbVlPUlI4NVRLZ2tXd1FJSmp3Nyszdnc0Z2NNRG5iOTRoS3MvSjFJc3FBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnVmJkWTI0c0RYS0c0S2h3WlBmOHpxVDRBU0ROamNUb2FFRi9MQnd2QS8xSUNcclxuSURiVmZCUk1PQVB5cWJkcytld1QwSDZqdDg1czZZTVNVZEo5Z2dmOWlmeTBcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9",
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
    "Referer": "https://www.douyin.com/",
}

# headers = {
#    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0',
#    'Cookie': 'sessionid=c6bb98799c00f7e99f00dafbecea0920;msToken=uTa38b9QFHB6JtEDzH9S4np17qxpG6OrROHQ8at2cBpoKfUb0UWmTkjCSpf72EcUrJgWTIoN6UgAv5BTXtCbOAhJcIRKyZIT7TMYapeOSpf;odin_tt=324fb4ea4a89c0c05827e18a1ed9cf9bf8a17f7705fcc793fec935b637867e2a5a9b8168c885554d029919117a18ba69; ttwid=1%7CWBuxH_bhbuTENNtACXoesI5QHV2Dt9-vkMGVHSRRbgY%7C1677118712%7C1d87ba1ea2cdf05d80204aea2e1036451dae638e7765b8a4d59d87fa05dd39ff; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVKUDZzbjNLRlFBNUROSEcyK2F4bXAwNG5cclxud1hBSTZDU1IyZW1sVUE5QTZ4aGQzbVlPUlI4NVRLZ2tXd1FJSmp3Nyszdnc0Z2NNRG5iOTRoS3MvSjFJc3FBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnVmJkWTI0c0RYS0c0S2h3WlBmOHpxVDRBU0ROamNUb2FFRi9MQnd2QS8xSUNcclxuSURiVmZCUk1PQVB5cWJkcytld1QwSDZqdDg1czZZTVNVZEo5Z2dmOWlmeTBcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; odin_tt=b55539d60124599d7788339a3fccf7e75fe95280f1d55cc572b9a02bdcdcf1d037a8db3ae525c69d8d0ff1dfd7a58167',
#    'Accept': '*/*',
#    'Host': 'www.douyin.com',
#    'Connection': 'keep-alive'
# }

def test():
    cookies = {
        "sessionid": "c6bb98799c00f7e99f00dafbecea0920",
    }
    resp = requests.get(url, headers=headers, cookies=cookies)
    print(resp.text)


def start_parse(dt):
    a = []
    for i in dt:
        if i.get("aweme_type") == 55:
            return i.get("desc")


def func(max_cursor=0, data: list = None):
    if not data:
        data = list()
    base_url = "https://www.douyin.com/aweme/v1/web/aweme/post/"
    sec_uid = "MS4wLjABAAAAw-MmWNqSSDu5O-sukdHy78GCEmxybtGoM87OOs7fuvE"
    single_count = 10
    aid = 6383
    params = {
        "sec_user_id": sec_uid,
        # "count": single_count,
        "max_cursor": max_cursor,
        "aid": aid,
    }
    cookies = {
        "sessionid": "c6bb98799c00f7e99f00dafbecea0920",
    }

    user_data = requests.get(base_url, params=params, cookies=cookies, headers=headers).json()

    data.append(start_parse(user_data.get("aweme_list", [])))
    if user_data.get("has_more"):
        return func(max_cursor=user_data.get("max_cursor"), data=data)

    return data


if __name__ == "__main__":
    url = "http://v26-web.douyinvod.com/ee15661672d89e41d42bcffe296f3ff7/64df9273/video/tos/cn/tos-cn-ve-15c001-alinc2/oseSEf2WDHGv3vkIT8LN3Qf5Ck3GIAEue7gMZA/?a=6383&ch=26&cr=0&dr=0&lr=all&cd=0%7C0%7C0%7C0&cv=1&br=2308&bt=2308&cs=0&ds=4&ft=bvTKJbQQqUuxfdoZPo0OW_EklpPiXE~HqMVJEwKyIcbPD-I&mime_type=video_mp4&qs=0&rc=aDVnOzlmNmY7aTk5MzU5OUBpM3dxN3U5cmh5bDMzNGkzM0BjMl9hLTIyXjIxLjYzXmNiYSNtc2FnMmRzMGtgLS1kLTBzcw%3D%3D&btag=e00028000&dy_q=1692369920&l=20230818224520074F6AD5D83AB822D708"
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0",
        "Referer": "https://www.douyin.com/",
    }

    resp = requests.head(url, headers=headers)
    # requests.request()
    print(resp.headers)
    # print(os.path.abspath(os.path.join("d:\\temp\\robin\\re", "..\\test\\..\\..\\..\\config.ini", "\\as")))
    # print(os.path.abspath(os.path.join("/temp/robin/re", "../test/../../../config.ini", "/as")))
