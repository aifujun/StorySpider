# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class XbiqugePipeline:

    def open_spider(self, spider):
        self.file = open('全职艺术家.txt', 'a', encoding='utf-8')


    def process_item(self, item, spider):
        info = ''.join(item['title']).strip()+'\n\n'+item['content']+'\n\f'
        self.file.write(info)
        # print(item)
        return item

    def close_spider(self, spider):
        self.file.close()
