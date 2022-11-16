import re

import requests
from lxml import etree
from threading import Thread
from queue import Queue


class MyThread(Thread):
    def __init__(self, q):
        Thread.__init__(self)
        self.q = q

    def run(self):
        global index
        while not self.q.empty():
            data = self.q.get()
            url = root + ''.join(data[1])
            response = requests.get(url, headers=headers)
            response.encoding = response.apparent_encoding
            page = etree.HTML(response.text)

            chapter = page.xpath('//div[@class="bookname"]/h1/text()')
            chapter = ''.join(chapter).strip()
            print(f"爬取: {index}-> 《{chapter}》")

            content = page.xpath("//div[@id='content']/text()")
            content = '\n'.join(content)
            content = content.replace("\xa0\xa0\xa0\xa0", "\t")
            content = re.sub(r'\n+', '\n', content)
            content = re.sub(r'\r+', '', content)
            content = re.sub(r'\r\n', '', content)
            content = re.sub(r'[ ]+', '', content)

            # 如果当前标记比保存的小说章节序号大于1，阻塞
            while data[0] > index + 1:
                pass

            # 刚好大于1时，通过，保存章节
            if data[0] == index + 1:
                print(f"保存: {index}-> 《{chapter}》")
                f.write(chapter + '\n')
                f.write(content + '\n\f\n')
                index += 1


if __name__ == '__main__':
    root = "https://www.ddxs.cc"
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    index = -1  # 章节标记，表示保存的章数

    response = requests.get(r'https://www.ddxs.cc/ddxs/176796/', headers=headers)
    response.encoding = response.apparent_encoding
    page = etree.HTML(response.text)
    title = ''.join(page.xpath('//*[@id="info"]/h1/text()'))  # 小说名
    print(title)

    with open("%s.txt" % title, 'w', encoding='utf8') as f:
        f.write(title)  # 先写入小说名
        hrefs = page.xpath('//*[@id="list"]/dl/dd/a/@href')
        q = Queue()
        for i, href in enumerate(hrefs):
            q.put((i, href))

        ts = []
        for i in range(5):
            t = MyThread(q)
            t.start()
            ts.append(t)
        for t in ts:
            t.join()
