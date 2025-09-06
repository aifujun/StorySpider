import os
import re
import requests
import traceback

from lxml import etree
from tqdm import tqdm

from src.common.logger import logger


class Spider(object):

    def __init__(self):
        pass

    def get_page(self, target_url):
        """
        获取当前章节页面信息

        Args:
            target_url:当前章节的链接
        Return:
            html:经lxml转换后的数据
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49 QIHU 360SE',
            'Cookie': '',
        }  # 头部伪装
        html = None
        try:
            resp = requests.get(target_url, headers=headers)
            resp.encoding = 'utf-8'
            html = etree.HTML(resp.text)
        except Exception as e:
            logger.exception(f'Get url: {target_url} page failed. exception: {e}')
        return html

    def get_book_info(self, book_url):
        """
        获取书本的信息

        Args:
            book_url:书本目录链接
        Return:
            None
        """
        try:
            html = self.get_page(book_url)
            title = html.xpath('//*[@id="info"]/h1/text()')[0].strip()
            # title = re.sub(r'\s', '', title)
            if not os.path.exists(r'Books\\' + title):
                os.mkdir(r'Books\\' + title)

            chapter_list = html.xpath('//*[@id="list"]/dl/dd/a/text()')
            chapter_num = len(chapter_list)
            chapter_href_list = html.xpath('//*[@id="list"]/dl/dd/a/@href')  # 每个章节链接
            for chapter, chapter_href in tqdm(zip(chapter_list, chapter_href_list), total=chapter_num):
                href = 'https://www.9biqu.com' + chapter_href
                self.download_book(title, chapter, href)
        except:
            print('未找到该信息\n')
            traceback.print_exc(file=open(r"../../../log/log.txt", 'a', encoding='utf-8'))

    def download_book(self, title, chapter, chapter_url):
        html = self.get_page(chapter_url)
        text_list = html.xpath('//*[@id="content"]/p/text()')
        text = "\n".join(text_list)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\r+', '', text)
        text = re.sub(r'\r\n', '', text)
        text = re.sub(r'[ ]+', '', text)
        file_name = 'Books\\' + title + '\\' + title + '.txt'
        # print("正在抓取文章：" + file_name + '\\' + chapter)
        with open(file_name, 'a', encoding="utf-8") as f:
            f.write(chapter + '\n' + text + '\n')

    def start(self, bool_url):
        self.get_book_info(bool_url)


if __name__ == "__main__":
    url = r'https://www.9biqu.com/biquge/23492'
    spider = Spider()
    spider.start(url)
