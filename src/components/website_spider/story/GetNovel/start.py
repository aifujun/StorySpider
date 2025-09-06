
from scrapy import cmdline


if __name__ == '__main__':
    cmdline.execute("scrapy crawl qustory -a initial_url=https://www.xbiquge.la/13/13320/".split(' '))
