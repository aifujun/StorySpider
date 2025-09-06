import scrapy

import re


class BqgSpider(scrapy.Spider):
    name = 'bqg'
    allowed_domains = ['xbiquge.la']
    start_urls = ['https://www.xbiquge.la/63/63436/25543205.html']

    def parse(self, response):
        title = response.xpath('//div[@class="bookname"]/h1/text()').get()
        content_list = response.xpath('//div[@id="content"]/text()').getall()
        content = '\n'.join(content_list)
        content = re.sub(r'\n+', '\n', content)
        content = re.sub(r'\r+', '', content)
        content = re.sub(r'\r\n', '', content)
        content = re.sub(r'[ ]+', '', content)
        # content = re.sub(r'\xa0\xa0\xa0\xa0', '    ', content)
        next_url = 'https://www.xbiquge.la' + response.xpath('//div[@class="bottem2"]/a[4]/@href').extract_first()

        yield {
            'title': title,
            'content': content,
        }

        yield scrapy.Request(next_url, callback=self.parse)
