import requests

from concurrent.futures import ThreadPoolExecutor
from lxml import etree
from threading import Thread, RLock
from queue import Queue

from tqdm import tqdm

from common.logger import logger
from spider.base.spider import Spider

__all__ = ["Downloader"]

porter_index = -1


class Porter(Thread):
    def __init__(self, queue_consumer: Queue, save_file: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue_consumer = queue_consumer
        self.save_file = save_file

    def run(self):
        global porter_index
        while not self.queue_consumer.empty():
            chapter_index, chapter, chapter_url = self.queue_consumer.get()
            logger.debug(f"爬取章节: {chapter_index} -> 《{chapter}》")

            page = Spider().get_html(chapter_url)
            content = page.xpath("//div[@id='content']/text()")
            content = '\n'.join(content)
            content = content.replace("\xa0\xa0\xa0\xa0", "\t")

            # 如果当前标记比保存的小说章节序号大于1，阻塞
            while chapter_index > porter_index + 1:
                pass
                continue

            # 刚好大于1时，通过，保存章节
            if chapter_index == porter_index + 1:
                logger.debug(f"保存: {chapter_index} ->《{chapter}》")
                with RLock():
                    self.save(chapter, content)
                    porter_index += 1

    def save(self, chapter, content):
        try:
            with open(self.save_file, 'w', encoding='utf-8') as file:
                file.write(chapter + '\n\n')
                file.write(content + '\n\f')
        except IOError as ioe:
            logger.exception(f"Save 《{chapter}》 failed, except: {ioe}")
            raise IOError(f"Save 《{chapter}》 failed.")


class Downloader(object):
    def __init__(self,
                 queue_consumer: Queue,
                 save_file: str,
                 thread_num: int = 200,
                 *args,
                 **kwargs):
        self.queue_consumer = queue_consumer
        self.save_file = save_file
        self.thread_num = thread_num

    def download(self, thread_num: int = None):
        thread_num = self.thread_num if thread_num is None else thread_num
        ts = []
        for i in range(thread_num):
            t = Porter(self.queue_consumer, self.save_file)
            t.start()
            ts.append(t)

        for t in ts:
            t.join()


if __name__ == '__main__':
    porter_index = -1  # 章节标记，表示保存的章数
