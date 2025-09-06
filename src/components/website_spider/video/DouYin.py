import os
import random
import string
from enum import Enum

from urllib.parse import urlparse

import execjs

from components.model.video_data import (ImageData, VideoData, MusicData, Info, MediaData, MixInfo, AuthorInfo,
                                         ParsedData, MediaType)
from components.website_spider.base.base_parser import BaseParser
from conf.config import Configuration, DYApiConfig


class AwemeType(Enum):
    GENERAL = 0
    IMAGE = 2
    VIDEO = 4
    IMAGE_VIDEO = 61
    VIDEO_TOGETHER = 66
    NOTE = 68
    SOCIAL_COMMON_PUBLISH = 109

    UNKNOWN = 55


class DouYinParser(BaseParser):
    def __init__(self):
        super().__init__(referer=DYApiConfig.index_url)
        self.url_base = DYApiConfig.url_base
        self.user_data_api = DYApiConfig.user_data_api
        self.video_data_api = DYApiConfig.video_data_api
        self.user_profile_api = DYApiConfig.user_profile_api
        self._aid = DYApiConfig.aid

        self._type = None
        self._type_id = None
        self.data_detail = dict()
        self.data = dict()

    @staticmethod
    def generate_random_str(length=107):
        """根据传入长度产生随机字符串"""
        random_str = ''
        base_str = string.ascii_letters + string.digits + '='
        for i in range(length):
            random_str += random.choice(base_str)
        return random_str

    @staticmethod
    def generate_x_bogus(url, user_agent):
        query = urlparse(url).query
        x_bogus = execjs.compile(open(Configuration.dy_x_bogus_js).read()).call('sign', query, user_agent)
        return x_bogus

    def get_data(self, timeout: int = 180):
        """根据链接获取数据

        :param timeout: 超时时间
        :return:
        """
        base_url = self.video_data_api.format(aid=self._aid, aweme_id=self._type_id, x_bogus="x_bogus")
        x_bogus = self.generate_x_bogus(base_url.split("&X-Bogus")[0], self.headers.get("User-Agent"))
        base_url = base_url.replace("x_bogus", x_bogus)

        data = self.get(base_url, timeout=timeout).json()

        return data.get("aweme_detail", {})

    def get_author_data(self, sec_user_id, timeout: int = 180) -> dict:
        base_url = self.user_profile_api.format(aid=self._aid, sec_user_id=sec_user_id, x_bogus="x_bogus")
        x_bogus = self.generate_x_bogus(base_url.split("&X-Bogus")[0], self.headers.get("User-Agent"))
        base_url = base_url.replace("x_bogus", x_bogus)

        data = self.get(base_url, timeout=timeout).json()

        return data.get("user", {})

    def set_cookie(self):
        self.headers["Cookie"] = DYApiConfig.cookies.format(ms_token=self.generate_random_str(107))

    def parse_init(self, share_text: str, timeout: int = 180):
        """初始解析，获取相关数据

        :param share_text: 待解析链接或分享的文本
        :param timeout: 超时时间
        :return:
        """
        share_url = self.extract_url_from_string(share_text)[0]
        tmp_resp = self.head(share_url, timeout=timeout)
        request_url_path = os.path.normpath(urlparse(tmp_resp.url).path)

        self._type = os.path.basename(os.path.dirname(request_url_path))
        self._type_id = os.path.basename(request_url_path)
        self.set_cookie()

        if self._type != "user":
            self.data_detail = self.get_data()

    def parse_author_info(self):
        """解析作者信息"""
        sec_uid = self._type_id if self._type == "user" else self.data_detail.get("author", {}).get("sec_uid")
        user_data = self.get_author_data(sec_uid)

        nickname = user_data.get("nickname", "")
        sec_uid = user_data.get("sec_uid", "")

        # 个性签名
        signature = user_data.get("signature", "")
        # 头像
        avatar_url_list = user_data.get("avatar_larger", {}).get("url_list", [])
        country = user_data.get("country", "")
        province = user_data.get("province", "")
        city = user_data.get("city", "")
        school_name = user_data.get("school_name", "") or ""
        # 主页封面
        cover_image_info = []
        for i in user_data.get("cover_and_head_image_info", {}).get("profile_cover_list", []):
            cover_image_info.append(i.get("cover_url", {}).get("url_list"))

        home = self.url_base.format(type="user", type_id=sec_uid)

        return AuthorInfo(nickname=nickname,
                          home=home,
                          signature=signature,
                          avatarUrlList=avatar_url_list,
                          country=country,
                          province=province,
                          city=city,
                          schoolName=school_name,
                          coverImageInfo=cover_image_info)

    def parse_mix_info(self):
        """解析合集信息"""
        mix_info = self.data_detail.get("mix_info", {})
        is_collection = True if mix_info else False

        cover_url_list = mix_info.get("cover_url", {}).get("url_list", [])
        mix_id = mix_info.get("mix_id", "")
        mix_name = mix_info.get("mix_name", "")
        desc = mix_info.get("desc", "")
        current_episode = mix_info.get("statis", {}).get("current_episode", 0)
        total_episode = mix_info.get("statis", {}).get("updated_to_episode", 0)
        return MixInfo(isCollection=is_collection,
                       mixId=mix_id,
                       mixName=mix_name,
                       desc=desc,
                       currentEpisode=current_episode,
                       totalEpisode=total_episode,
                       coverUrlList=cover_url_list)

    def parse_info(self):
        """解析详细信息"""
        desc = self.data_detail.get("desc")
        author = self.data_detail.get("author", {}).get("nickname", "")
        aweme_type = MediaType.note if self._type == MediaType.note.name else MediaType.video
        origin_url = self.url_base.format(type=aweme_type.name, type_id=self.data_detail.get("aweme_id"))

        return Info(originUrl=origin_url,
                    type=aweme_type.value,
                    author=author,
                    desc=desc,
                    mixInfo=self.parse_mix_info())

    def parse_image(self):
        """开始解析图集"""
        images = self.data_detail.get("images")
        if not images:
            return ImageData()

        url_list = [img.get("url_list") for img in images]
        return ImageData(urlList=url_list)

    def parse_music(self):
        """开始解析背景音乐"""
        music = self.data_detail.get("music", {})
        name = music.get("title")
        author = music.get("author")
        album = music.get("album")
        url = music.get("play_url", {}).get("uri", "")

        return MusicData(name=name, author=author, album=album, url=url)

    def parse_video(self):
        """开始解析视频"""
        data_size = self.data_detail.get("video", {}).get("play_addr", {}).get("data_size", 0)
        url_list = self.data_detail.get("video", {}).get("play_addr", {}).get("url_list") if data_size else []
        cover_url_list = self.data_detail.get("video", {}).get("origin_cover", {}).get("url_list", [])

        return VideoData(dataSize=data_size, urlList=url_list, coverUrlList=cover_url_list)

    def parse_user(self, max_cursor: int = 0, data: list = None, count: int = 10):
        """解析主页分享链接
        """
        if not data:
            data = list()

        base_url = self.user_data_api.format(
            sec_user_id=self._type_id,
            count=count,
            max_cursor=max_cursor,
            aid=self._aid
        )

        user_data = self.get(base_url).json()

        for i in user_data.get("aweme_list", []):
            self.data_detail = i
            data.append(self.start_parse())
        if user_data.get("has_more"):
            return self.parse_user(max_cursor=user_data.get("max_cursor"), data=data)

        return data

    def start_parse(self):
        data = MediaData(info=self.parse_info(),
                         music=self.parse_music(),
                         images=self.parse_image(),
                         video=self.parse_video())
        return data

    def parse(self, share_text: str, timeout: int = 180):
        """根据链接获取渲染数据

        :param share_text:
        :param timeout:
        :return:
        """
        self.parse_init(share_text, timeout)

        if self._type == "user":
            data = self.parse_user()
        else:
            data = [self.start_parse()]

        parsed_data = ParsedData(authorInfo=self.parse_author_info(),
                                 data=data)
        self.data = parsed_data.json(ensure_ascii=False)
        return parsed_data


if __name__ == "__main__":
    # text = "https://www.douyin.com/note/7228793018789219618"
    text = "https://www.douyin.com/video/7252695782170873088"
    txt = "https://www.douyin.com/user/MS4wLjABAAAAw-MmWNqSSDu5O-sukdHy78GCEmxybtGoM87OOs7fuvE"
    tx = "1.23 BtR:/ 【KANSAI】前三位都在各自的领域占有一席之地，第一位是顶级花魁 # 时装秀 # 穿搭 # 花魁 # 铃木爱 # 颜值  https://v.douyin.com/iauxLLX/ 复制此链接，打开Dou音搜索，直接观看视频！"

    tiktok: DouYinParser = DouYinParser()
    tiktok.parse(text)

    print(tiktok.data)
    # with open("a.txt", "w", encoding="utf-8") as f:
    #     f.write(str(tiktok.data))
