import re
import traceback

from tqdm import tqdm

from src.common.logger import get_logger
from spider.base.spider import Spider

log = get_logger()


class NovelSpider(Spider):
    def __init__(self, **kwargs):
        """

        Args:
            **kwargs: 
        """
        super().__init__(**kwargs)

    def get_book_info(self, book_url):
        """
        获取书本的信息

        Args:
            book_url:书本目录链接
        Return:
            None
        """
        html = self.get_html(book_url)
        # 获取书名
        title = html.xpath('//*[@id="info"]/h1/text()')[0]
        chapter_list = html.xpath('//*[@id="list"]/dl/dd/a/text()')
        href_list = html.xpath('//*[@id="list"]/dl/dd/a/@href')
        chapters = []
        for chapter, href in zip(chapter_list, href_list):
            chapters.append((chapter, href))
        return title, chapters

    def get_chapter_content(self, chapter_href):
        """
        获取书本的信息
            Args:
                chapter_href: 章节链接
            Return:
        """
        try:
            url = 'https://www.xbiquge.la/68/68873/27313549.html'
            html = self.get_html(chapter_href)
            chapter_list = html.xpath('//ul[@class="cf"]/li/a/text()')  # 爬取章节目录
            chapter_num = len(chapter_list)
            chapter_href_list = html.xpath('//ul[@class="cf"]/li/a/@href')  # 每个章节链接
            for chapter, chapter_href in tqdm(zip(chapter_list, chapter_href_list), total=chapter_num):
                chapter = re.sub(r'\s', '', chapter)
                href = 'https:' + chapter_href
                self.DownloadBook(title, chapter, href)
        except:
            traceback.print_exc(file=open(r"../../../log/log.txt", 'a', encoding='utf-8'))

    def download_book(self, title, chapter, chapter_url):
        html = self.GetPages(chapter_url)
        text_list = html.xpath('//div[@class="read-content j_readContent"]/p/text()')
        text = "\n".join(text_list)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\r+', '', text)
        text = re.sub(r'\r\n', '', text)
        text = re.sub(r'[ ]+', '', text)
        file_name = 'Books\\' + title + '\\' + title + '.txt'
        # print("正在抓取文章：" + file_name + '\\' + chapter)
        with open(file_name, 'a', encoding="utf-8") as f:
            f.write(chapter + '\n' + text)


def Download():
    url = r'https://www.xbiquge.la/11/11433/'
    spider = NovelSpider()
    spider.get_book_info(url)


if __name__ == "__main__":
    Download()

