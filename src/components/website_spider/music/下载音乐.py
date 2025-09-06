import os
import requests
import json
import time
import traceback
from tqdm import tqdm


class MusicSpider:
    def get_page(self):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
                # 'Referer':'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
                'csrf': 'IV9C8YJA11',
                'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1603461123; _ga=GA1.2.716489643.1603461123; _gid=GA1.2.1633576714.1603461123; reqid=7c6c4c66X6a47X44a4Xa7b9X85072188ffb0; gtoken=QGWMzDK6SeQV; gid=b3d74f5a-564f-4b4d-be85-022e310107ec; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1603461216; kw_token=IV9C8YJA11'
            }

            singer, page_num = self.Search_info()
            if singer not in os.listdir('.\\音乐'):
                os.mkdir('.\\音乐\\' + singer)

            for page in range(1, 1 + page_num):
                url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&reqID=615ae920-2d21-11ea-b560-73e04c9f8018'.format(
                    singer, page)
                resp = requests.get(url, headers=headers)
                result = json.loads(resp.text)
                data = result['data']['list']

                for music in tqdm(data, total=len(data) * page_num):
                    self.down_music(singer, music, headers)

        except Exception as e:
            traceback.print_exc(e)
            print('获取网页数据错误')

    def down_music(self, singer, music, headers):

        # 音乐的ID
        rid = music['rid']
        # 音乐的名称
        name = music['name']
        # 爬取到指定歌手歌曲的音乐路径
        url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1577081015618&reqID=f4af2221-2549-11ea-92dc-b1e779c8d1d6'.format(
            rid)
        result = requests.get(url, headers=headers).json()
        # print(result.text)
        # result=result.json()
        # 音乐路径
        music_url = result['url']
        time.sleep(2)
        # 下载音乐
        file_name = '.\\音乐\\' + singer + '\\{}.mp3'.format(name)
        with open(file_name, 'wb') as f:
            music = requests.get(music_url, headers=headers)  # 获取音乐文件
            time.sleep(2)
            f.write(music.content)  # 转格式
            f.close()
            # print('\t下载完成')

    def Search_info(self):
        singer = str(input('请输入歌手的名称：'))
        page_num = int(input('请输入要下载页数：'))
        return singer, page_num


if __name__ == '__main__':
    down = MusicSpider()
    down.get_page()
