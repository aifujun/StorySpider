
import requests


music_url = 'http://stream10.qqmusic.qq.com/101790422.wma'
url1 = 'https://dl.stream.qqmusic.qq.com/C400002gkvts3G55ur.m4a?guid=5738729978&vkey=FE7E4117B4961ADAFCBEEEEB36C3313200C7B2EC47E457B4F98A07D0210B628D1C8E7C0E1F9B63F5AC91329918B1B124A30A93588905C850&uin=&fromtag=66'
url = 'https://y.qq.com/n/ryqq/search?w=%E5%8D%83%E7%99%BE%E9%A1%BA&t=song'
headers = {
    'Referer': 'https://y.qq.com/portal/search.html',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',

}

file_name = '很任性.wma'
with open(file_name, 'wb') as f:
    music = requests.get(music_url, headers=headers)
    f.write(music.content)
    f.close()