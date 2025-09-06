
import requests
import json
import time


def main():
    singer = str(input('请输入歌手的名称：'))
    number = int(input('请输入要下载页数：'))
    for x in range(1, number + 1):
        # 该网站有反爬机制，要用模拟浏览器来进行伪装。
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
            'Referer': 'http://www.kuwo.cn/search/list?key=%E5%91%A8%E6%9D%B0%E4%BC%A6',
            'csrf': 'IV9C8YJA11',
            'Cookie': 'Hm_lvt_cdb524f42f0ce19b169a8071123a4797=1603461123; _ga=GA1.2.716489643.1603461123; _gid=GA1.2.1633576714.1603461123; reqid=7c6c4c66X6a47X44a4Xa7b9X85072188ffb0; gtoken=QGWMzDK6SeQV; gid=b3d74f5a-564f-4b4d-be85-022e310107ec; _gat=1; Hm_lpvt_cdb524f42f0ce19b169a8071123a4797=1603461216; kw_token=IV9C8YJA11'
        }
        # json 逆向解析api接口  音乐接口
        url = 'http://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={}&pn={}&rn=30&reqID=615ae920-2d21-11ea-b560-73e04c9f8018'.format(
            singer, x)
        rest = requests.get(url, headers=headers)
        result = json.loads(rest.text)
        data = result['data']['list']
        print(data)
        for i in data:
            # 音乐的ID
            rid = i['rid']
            # 音乐的名称
            name = i['name']
            # 爬取到指定歌手歌曲的音乐路径
            url = 'http://www.kuwo.cn/url?format=mp3&rid={}&response=url&type=convert_url3&br=128kmp3&from=web&t=1577081015618&reqID=f4af2221-2549-11ea-92dc-b1e779c8d1d6'.format(
                rid)
            result = requests.get(url, headers=headers)  # .json()
            print(result.text)
            result = result.json()
            # 音乐路径
            music_url = result['url']
            time.sleep(2)
            # 下载音乐
            with open('酷我音乐/{}.mp3'.format(name), 'wb') as f:
                music = requests.get(music_url, headers=headers)  # 获取音乐文件
                time.sleep(2)
                f.write(music.content)  # 转格式
                f.close()
                print('\t下载完成')


main()
