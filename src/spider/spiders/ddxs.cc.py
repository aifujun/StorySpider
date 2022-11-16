import os
import re
from queue import Queue
from typing import Tuple, Any

import requests
import traceback

from lxml import etree
from tqdm import tqdm

from common.errCode import ErrorCode
from common.logger import logger
from spider.base.downloader import Downloader
from spider.base.spider import Spider


class DdxsSpider(Spider):

    def __init__(self, index_url: str, book_url: str):
        super().__init__()
        self.index_url = index_url
        self.book_url = book_url
        self.save_file = None
        self.chapter = None
        self.book_name = None
        self.author = None
        self.introduction = None
        self.get_book_info()

    def get_book_info(self):
        """
        获取书本的信息

        Return:
            None
        """
        book_info = None
        html = self.get_html(self.book_url)
        if html is None:
            return ErrorCode.GET_HTML_ERROR.value, book_info
        self.book_name = html.xpath('//*[@id="info"]/h1/text()')[0].strip()
        self.author = html.xpath('//*[@id="info"]/p[1]/text()')[0].split(":")[-1].strip()
        self.introduction = html.xpath('//*[@id="intro"]/p/text()')[0].strip()
        chapter_list = html.xpath('//*[@id="list"]/dl/dd/a/text()')
        chapter_href_list = html.xpath('//*[@id="list"]/dl/dd/a/@href')
        self.chapter = list(zip(chapter_list, chapter_href_list))
        book_info = {
            'book_name': self.book_name,
            'author': self.author,
            'introduction': self.introduction,
            'chapter': self.chapter
        }
        return book_info

    def get_chapter(self, page_html, **kwargs) -> tuple[str, str]:
        # 章节名
        chapter_name = page_html.xpath('//div[@class="bookname"]/h1/text()')[0]
        # 章节列表
        chapter_contents = page_html.xpath('//div[@id="content"]/text()')
        tmp_contents = []
        for content in chapter_contents:
            content = re.sub(r'[\r\n\t\s]+', '', content)
            if content:
                tmp_contents.append(content)
        tmp_contents[0] = f'\t{tmp_contents[0]}'
        chapter_content = '\n\n\t'.join(tmp_contents)

        return chapter_name, chapter_content

    def save(self, chapter, content):
        try:
            with open(self.save_file, 'a+', encoding='utf-8') as file:
                file.write(chapter + '\n\n')
                file.write(content + '\n\f')
        except IOError as ioe:
            logger.exception(f"Save 《{chapter}》 failed, except: {ioe}")
            raise IOError(f"Save 《{chapter}》 failed.")

    def download_book(self):
        queue_producer = Queue()
        loop = tqdm(enumerate(self.chapter), total=len(self.chapter))
        for index, (chapter, chapter_href) in loop:
            # print(chapter, chapter_href)
            queue_producer.put((index, chapter, f"{self.index_url}{chapter_href}"))
        downloader = Downloader(queue_producer, save_file="./test.txt")
        downloader.download()

    def start(self):
        self.get_book_info()


if __name__ == "__main__":
    ind_url = r'https://www.ddxs.cc'
    url = r'https://www.ddxs.cc/ddxs/176796/'
    spider = DdxsSpider(ind_url, url)
    spider.download_book()
