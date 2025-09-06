
import re

import scrapy

from tqdm import tqdm
from story.items import StoryItem


class QuStorySpider(scrapy.Spider):
    name = 'qustory'
    allowed_domains = ['xbiquge.la']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.book_name = None
        self.start_urls = [kwargs.get('initial_url', '')]

    def parse(self, response, **kwargs):
        self.book_name = response.xpath('//div[@id="info"]/h1/text()').extract_first()
        chapter_href_list = response.xpath('//div[@id="list"]/dl/dd/a/@href').extract()
        for index, chapter_href in enumerate(tqdm(chapter_href_list, desc='Downloading')):
            chapter_url = 'https://www.xbiquge.la' + chapter_href
            yield scrapy.Request(chapter_url, callback=self.parse_content, cb_kwargs={'index': index})

    def parse_content(self, response, index):
        chapter_title = response.xpath('//div[@class="bookname"]/h1/text()').extract_first()
        content = response.xpath('//div[@id="content"]/text()').extract()
        content = self.format_content(content)

        item = StoryItem()
        item['book_name'] = self.book_name
        item['index'] = index
        item['chapter_title'] = chapter_title
        item['content'] = content

        yield item

    @staticmethod
    def format_content(content: list) -> str:
        """
        对爬取的章节内容合并，格式化

        :param content: 章节内容列表
        :return: 格式化后的章节字符串
        """
        content = ''.join(content)
        content = re.sub('\xa0\xa0\xa0\xa0', '\t', content)
        content = re.sub('\r+', '\n', content)
        content = re.sub('\n+', '\n', content)
        content = re.sub('\r\n', '', content)

        return content

