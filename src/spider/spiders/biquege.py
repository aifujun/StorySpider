import scrapy


class BiquegeSpider(scrapy.Spider):
    name = 'biquege'
    allowed_domains = ['www.xbiquge.la']
    start_urls = ['https://www.9biqu.com/biquge/23492']

    def parse(self, response):
        pass
