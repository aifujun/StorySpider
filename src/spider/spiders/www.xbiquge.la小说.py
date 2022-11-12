"""
Author: aifujun
Date: 2021-07-18 14:23:58
LastEditTime: 2021-07-18 15:33:15
LastEditors: aifujun
Description:
FilePath: /GetNovel/www.xbiquge.la小说.py
Copyright 2021 fujun
春雨夏风秋云冬雪
"""

import os
import re
import requests
import time
import traceback

from lxml import etree
from tqdm import tqdm


class spider(object):

    def __init__(self, master=None):
        self.CreatLog()

    def GetTime(self):
        '''获取当前时间'''
        localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        #print(localtime)
        return localtime

    def CreatLog(self):
        '''创建请求日志文件'''
        if 'log' not in os.listdir('../../..'):
            os.mkdir(r"../../../log")
        with open(r"../../../log/log.txt", 'a', encoding ='utf-8') as f:
            f.write('-------------------' + self.GetTime() + '-------------------\n')
            f.close()

    def GetPage(self, url):
        '''
        获取当前章节页面信息
            Args:
                url:当前章节的链接
            Return:
                html:经lxml转换后的数据
        '''
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.49 QIHU 360SE',
            'Cookie':'',
        }    #头部伪装
        
        try:
            resp = requests.get(url, headers=headers)
            resp.encoding = 'utf-8'
            html = etree.HTML(resp.text)
        except Exception as e:
            print(url+" 请求错误\n", e)
            traceback.print_exc(file = open(r"../../../log/log.txt", 'a', encoding='utf-8'))
        else:
            return html

    def GetBookInfo(self, book_url):
        '''
        获取书本的信息
            Args:
                book_url:书本目录链接
            Return:
                None
        '''
        try:
            html = self.GetPage(book_url)
            title = html.xpath('//*[@id="info"]/h1/text()')[0]
            title = re.sub(r'\s', '', title)
            if os.path.exists(r'Books\\' + title) == False:
                os.mkdir(r'Books\\' + title)

            chapter_list = html.xpath('//*[@id="list"]/dl/dd/a/text()')
            chapter_num = len(chapter_list)
            chapter_href_list = html.xpath('//*[@id="list"]/dl/dd/a/@href')  #每个章节链接

            file_name = 'Books\\' + title + '\\' + title + '.txt'
            f = open(file_name, 'a', encoding="utf-8")

            for chapter, chapter_href in tqdm(zip(chapter_list, chapter_href_list), total = chapter_num):
                href = 'https://www.xbiquge.la' + chapter_href
                text = self.DownloadBook(href)
                f.write(chapter + '\n\n' + text + '\n\n\f')
        except:
            print('未找到该信息\n')
            traceback.print_exc(file = open(r"../../../log/log.txt", 'a', encoding ='utf-8'))
        else:
            f.close()

    def DownloadBook(self, chapter_url):
        html = self.GetPage(chapter_url)
        text_list = html.xpath('//*[@id="content"]/text()')
        text = '\n'.join(text_list)
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\r+', '', text)
        text = re.sub(r'\r\n', '', text)
        text = re.sub(r'[ ]+', '', text)
        return text

    def start(self, url):
        self.GetBookInfo(url)


if __name__ == '__main__':
    url = r'https://www.xbiquge.la/11/11433/'
    spider = spider()
    spider.start(url)







