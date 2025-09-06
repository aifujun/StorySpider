# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StoryPipeline:
    def __init__(self):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        self.items.sort(key=lambda i: i['index'])
        book_name = self.items[0].get('book_name')
        try:
            with open(f'./books/{book_name}.txt', 'w+', encoding='utf-8') as f:
                for item in self.items:
                    contents = ''.join(item.get('chapter_title')).strip() + '\n\n' + item.get('content') + '\n\n'
                    f.write(contents)
        except IOError as ioe:
            print(ioe)
        finally:
            f.close()
