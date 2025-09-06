import os
import time
from enum import Enum
from urllib.parse import unquote, urlparse

import requests

from common.regular_expression import RegExpression
from conf.content_type import content_type_map
from manager.publisher import Publisher


class DownloadStatus(Enum):
    SUCCESS = 0
    INITIALIZING = 1
    DOWNLOADING = 2
    PAUSE = 3

    FAILED = -1
    CANCELED = -2


class FileMode(Enum):
    APPEND_BIN = 'ab'
    WRITE_BIN = 'wb'
    READ_ONLY = 'r'


class Downloader:
    def __init__(self,
                 url: str,
                 save_path: str,
                 *,
                 referer: str = None,
                 cookies: str = None,
                 publisher: Publisher = Publisher()):
        """创建一个下载器

        :param url: 下载链接
        :param save_path: 文件下载保存目录
        :param referer: 下载某些特殊链接需要的 referer
        :param cookies: 下载某些特殊链接需要的 cookies
        :param publisher: 进度上报器
        """

        self.url = url
        self.save_path = save_path
        self.headers = {
            'Referer': referer,
            'Cookie': cookies,
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0"
        }
        self.publisher = publisher

        self.filename = None
        self.file_size = None
        self.file_type = None

        self.flag = True
        self.status = DownloadStatus.INITIALIZING.value
        self.file_mode = FileMode.WRITE_BIN.value
        self.header_flag = False
        self.chunk_size = 1024 * 1024

        self.initialize()

    @staticmethod
    def save_file(data, filename):
        try:
            with open(filename, "wb") as f:
                f.write(data)
        except OSError:
            pass

    def get_file_type(self, resp_head):
        """获取文件类型"""
        if self.filename and "." in self.filename:
            return self.filename.split(".")[-1]

        if "Content-Type" in resp_head.headers:
            content_type = resp_head.headers.get('Content-Type').split(';')[0]
            return content_type_map.get(content_type)

        return "unknown"

    def get_filename(self, resp_head):
        """获取下载文件名"""
        if self.filename:
            return self.filename

        if 'Content-Disposition' in resp_head.headers:
            content_desc = resp_head.headers.get('Content-Disposition')
            filename = RegExpression.content_desc_filename.search(content_desc).group()
            return unquote(filename, encoding='utf8')

        return os.path.basename(os.path.normpath(urlparse(resp_head.url).path)) or "unknown"

    def initialize(self, timeout=180):
        resp_head = requests.head(self.url, headers=self.headers, allow_redirects=True, timeout=timeout)
        self.filename = self.get_filename(resp_head)
        self.file_type = self.get_file_type(resp_head)
        self.file_size = int(resp_head.headers.get('Content-Length', 0))

    def download(self, filename: str = None, save_path: str = None):
        filename = filename or self.filename
        save_path = save_path or self.save_path
        save_file = os.sep.join([save_path, filename])
        self.file_mode = 'wb'
        if os.path.exists(save_file) and self.header_flag:
            self.headers['Range'] = 'bytes={range_start}-{range_end}'.format(range_start=os.path.getsize(save_file),
                                                                             range_end='')
            self.file_mode = 'ab'
        resp = requests.get(self.url, stream=True, headers=self.headers)
        with open(save_file, self.file_mode) as f:
            for chunk in resp.iter_content(chunk_size=self.chunk_size):
                if chunk and self.flag:
                    f.write(chunk)
                else:
                    break
        time.sleep(1)

    def pause(self):
        pass

    def cancel(self, filename):
        """取消下载

        :param filename:
        :return:
        """
        self.status = DownloadStatus.CANCELED.value
        time.sleep(0.1)
        if os.path.isfile(filename):
            os.remove(filename)

    def download_image(self, url, save_file, progress):
        resp = requests.get(url)
        self.save_file(resp.content, save_file)
        self.publisher.update(progress)

    def download_video(self, url, save_file):
        chunk_size = 1024 * 1024
        resp = requests.get(url, stream=True)
        for chunk in resp.iter_content(chunk_size=chunk_size):
            self.save_file(chunk, save_file)
            self.publisher.update(chunk_size)


def start():
    url = "http://sns-video-al.xhscdn.com/stream/110/258/01e4742563be554a010376038865b3ac92_258.mp4"
    path = r"C:\Users\fujun\Desktop\as"

    downloader = Downloader(url, save_path=path)
    downloader.download()


if __name__ == "__main__":
    start()
