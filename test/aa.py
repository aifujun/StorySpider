import re  # 正则模块
import requests
from lxml import etree
import threading  # 多进程
from queue import Queue  # 队列
import cn2an  # 中文转阿拉伯数字  一 二 三  ---> 1 2 3


# 请求url
def get_url(url):
    response = requests.get(url=url, headers=headers)
    html = etree.HTML(response.text)
    return html


# 定义小说正文清理的函数
def data_clean(url):
    # 获取小说章节名称
    title_name = url.xpath('//h1/text()')[0]  # 获取小说的名称
    # 获取章节小说正文
    lis = []
    txt_list = url.xpath('//div[@id="content"]/text()')
    # 对小说正文进行处理
    for txt in txt_list:
        i = txt.replace('\t', '').replace('\n', '').replace('\r', '').replace('\u3000', '')
        lis.append(i)
    txt_list = str(lis)[2:-2].replace(r"'", '').replace(r', (=),', '').replace("。,", '。\n')
    return title_name, txt_list


# 保存
def save(Fiction_data):
    # 对字典的k按照升序规则进行排序
    Fiction_data = dict(sorted(Fiction_data.items()))
    # 保存
    for v in Fiction_data.values():
        with open(f'{T_name}.txt', 'a', encoding='utf-8') as fp:
            fp.write(str(v))


# 创建生产者类
class Productor(threading.Thread):
    # 定义初始化函数
    def __init__(self, URL_queue, DATA_queue):
        # 处理父类init
        threading.Thread.__init__(self)
        self.URL_queue = URL_queue  # 定义保存url的队列
        self.DATA_queue = DATA_queue  # 定义存储章节url请求结果的队列

    # 重写run方法
    def run(self):
        # 从队列中取出数据
        while not self.URL_queue.empty():
            url = self.URL_queue.get()

            # 请求并获取数据
            self.get_content(url)  # 请求取出的数据

    # 定义获取数据函数
    def get_content(self, url):
        # 请求单个小说文章页面
        html = get_url(url)
        self.DATA_queue.put(html)


# 创建消费者类,作用：从队列中取出数据，并保存
class Consumer(threading.Thread):
    # 定义初始化函数
    def __init__(self, DATA_queue):
        threading.Thread.__init__(self)
        self.DATA_queue = DATA_queue  # 定义取数据的队列

    # 重写run方法
    def run(self):
        while not self.DATA_queue.empty():
            if switch == 1:
                break
            try:
                html = self.DATA_queue.get(timeout=10)
                # DATA_queue数据解析
                tible, txt = data_clean(html)
                txt = tible + "\n" + txt + "\n"
                """
                由于是多线程，无法保证章节是顺序进行---处理方式：
                    1：建立一个字典保存小说内容
                    2：k：（将章节名称更换成阿拉伯数字）
                    3：v：（此章节对应的正文内容）   
                    4：最后对字典的键进行排序，解决问题。
                """
                # 取出章节名
                table_num = re.match(r'第(.*?)章', tible)
                # 防止部分章节 以阿拉伯数字命名
                if type(table_num) == int:
                    continue
                # 大写数字转换成阿拉伯数字
                table_num = cn2an.cn2an(table_num.group(1), "normal")
                print("下载的章节序号>>>>>>>>>>>>>>>>>>", table_num)
                # 以k v 的形式保存数据
                Fiction_data.update({table_num: txt})
            except Exception as e:
                print(f'{e}出错')

    def __del__(self):
        print("全部章节下载完成--程序退出,线程{}结束任务".format(threading.current_thread()))


if __name__ == '__main__':
    # 定义开关 目前为 关
    switch = 0
    # 定义保存小说的字典
    Fiction_data = {}
    # 小说主路由
    url = 'https://www.biquge.com/135_135772/'  # 测试路由
    # url = input("请输入您想爬取的小说路由：")
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3823.400 QQBrowser/10.7.4307.400',
    }
    # 定义保存url的队列
    URL_queue = Queue(3000)
    # 定义存储章节url请求结果的队列
    DATA_queue = Queue(3000)
    html_text = get_url(url)
    dt_url = html_text.xpath('//dt[2]/following-sibling::dd/a/@href')  # 获取所有的href标签 --未拼接版本
    # 遍历获取到的未拼接版本 然后进行路径拼接
    for url in dt_url:
        # 路径拼接
        url = 'https://www.biquge.com' + url  # 获取到所有完整的url
        # 将拼接好的路径，添加到队列中
        URL_queue.put(url)

    # 获取要爬取小说的名称
    T_name = html_text.xpath('//h1/text()')[0]

    p_list = []  # 生产者线程列表
    c_list = []  # 消费者线程列表
    # 创建五个线程
    for i in range(5):
        p = Productor(URL_queue, DATA_queue)
        c = Consumer(DATA_queue)
        p_list.append(p)
        c_list.append(c)
        p.start()
        c.start()

    # 阻塞生产者
    for p in p_list:
        p.join()

    # 定义开关 目前为 开
    switch = 1

    # 阻塞消费者
    for c in c_list:
        c.join()

    # 所有的线程执行完毕后，执行保存文件的函数
    save(Fiction_data)
