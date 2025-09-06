import json
import os

from urllib import parse
from urllib.parse import urlparse

from common.regular_expression import RegExpression
from components.model.video_data import ImageData, VideoData, MusicData, Info, MediaData, MixInfo, AuthorInfo, \
    ParsedData
from components.website_spider.base.base_parser import BaseParser


class DouYinParser(BaseParser):
    def __init__(self,
                 url_base="https://www.douyin.com/{type}/{type_id}",
                 ):
        super().__init__()
        self.url_base = url_base

        self._type = None
        self._data_key = None
        self.parsed_url = None
        self.data = dict()
        self.render_data = dict()
        self.data_detail = dict()

        self.headers["Cookie"] = "ttwid=1%7C5grcQhcCKwqv-Xs9lsffIaLJcUnQcZ4xfprzwayDvQM%7C1676605769" \
                                 "%7C255eb8db183847f6fd5f2cacf7d6549d63bf4969d381c3418e35995ac7b6a171; " \
                                 "passport_csrf_token=a83047d9ee4fd31aba58f70e304335a0; " \
                                 "passport_csrf_token_default=a83047d9ee4fd31aba58f70e304335a0; " \
                                 "s_v_web_id=verify_le7zsch1_vrWqCyLv_4vsJ_4Wbu_8f9O_8uaRdVZujUR1; " \
                                 "SEARCH_RESULT_LIST_TYPE=%22single%22; download_guide=%223%2F20230224%22; " \
                                 "xgplayer_user_id=262468157771; douyin.com; strategyABtestKey=%221677545888.188%22; " \
                                 "csrf_session_id=1b878a71d301ca0b9d1107a00a3237b2; " \
                                 "bd_ticket_guard_client_data" \
                                 "=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiI" \
                                 "tLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0N" \
                                 "RWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtv" \
                                 "Wkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUV3Z21Gc3VDVHZESjZZeE11eVdXTEJUNGtcclxuUUtDSGpBdU" \
                                 "9GeTV4Mno5QTFHMG9acTVuaVg0TzVPb2p5SFBVRnZBL0xOSzVaTWJ5bERtWmVhcWcwUnkzbjZBc1xyXG" \
                                 "5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMH" \
                                 "dDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnUG1rUzJQNUNBa1FRdU9GbnYraXFMZ0ZWNkxkMlBnQlA" \
                                 "4VlZpRXgvNXVyc0NcclxuSUVMMnVuMkIzSjBSOTdUazJ0VjB5RGZsLzBLaFk0TmR1WTkxL0g3Z0h3RFFc" \
                                 "clxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; VIDEO_FILTER_MEMO_SELE" \
                                 "CT=%7B%22expireTime%22%3A1678152445204%2C%22type%22%3A1%7D; __ac_nonce=063fd5b3f0" \
                                 "054f9ad1de6; __ac_signature=_02B4Z6wo00f011gMORgAAIDBHxoHtvE1a5tYLD2AALYJmzmLAnh" \
                                 "JfJGYj6YrdcJ.GqhXaYlXaOHrARLl6HXYMHjHJ5EWjjeLDHp7exvMavnxqmZ1k5C4LKe.PSfjtAe7p4E" \
                                 "8d.hBCkppHfice8; home_can_add_dy_2_desktop=%221%22; msToken=_zLGCd1OJcoYpZ-fRniWO" \
                                 "N1mH0QRLDV7QQDLZykyk-yi8iSN42r6xVyLhsC-yqr8O32mGA5d3TO1dLkHXF-BFdActIDv9RKjVe-yQO" \
                                 "RkllVOJqEkcJel5Q==; tt_scid=uk9.KTlPKHn.6qP2KcGIDFZUhII2O4vjDjErsTW866.w2Rux9NSFE" \
                                 "VtnQ6ia9htH733a; msToken=nY0Gi1G71gNPaoixSC3WbdsEB1sz6dOm4H2crksAfDH5aSI3EY_YwcGZ" \
                                 "h9xnDaVlu3rzTXh7PFbWjEuepynneEMYisoZrzpTxovmnb3U1zM9gFTwG3_VSg== "

    def get_render_data(self, parsed_url, timeout: int = 180):
        """根据链接获取渲染数据

        :param parsed_url: 解析后的真正视频链接
        :param timeout: 超时时间
        :return:
        """
        resp = self.get(parsed_url, timeout=timeout)
        # html过大导致lxml解析失败, 可以使用bs4或正则解析
        render_data = RegExpression.douyin_render_data.search(resp.text).group()
        self.render_data = json.loads(parse.unquote(render_data))
        for key in self.render_data.keys():
            if key not in ["_location", "app"]:
                self._data_key = key
                break
        return self.render_data

    def parse_init(self, share_text: str, timeout: int = 180):
        """初始解析，获取相关数据

        :param share_text: 待解析链接或分享的文本
        :param timeout: 超时时间
        :return:
        """
        share_url = self.extract_url_from_string(share_text)[0]
        tmp_resp = self.head(share_url, timeout=timeout)
        request_url_path = urlparse(tmp_resp.url).path
        type_id = os.path.basename(request_url_path)

        self._type = os.path.basename(os.path.dirname(request_url_path))
        self.parsed_url = self.url_base.format(type=self._type, type_id=type_id)
        self.get_render_data(self.parsed_url)
        self.data_detail = self.render_data.get(self._data_key, {}).get("aweme", {}).get("detail", {})

    def parse_mix_info(self):
        """解析合集信息"""
        mix_info = self.data_detail.get("mixInfo", {})
        cover_url = mix_info.get("cover", "")
        mix_id = mix_info.get("mixId", "")
        mix_name = mix_info.get("mixName", "")
        current_episode = mix_info.get("currentEpisode", 0)
        total_episode = mix_info.get("totalEpisode", 0)
        is_collection = True if total_episode else False
        return MixInfo(isCollection=is_collection,
                       coverUrl=cover_url,
                       mixId=mix_id,
                       mixName=mix_name,
                       currentEpisode=current_episode,
                       totalEpisode=total_episode)

    def parse_author_info(self):
        """解析作者信息"""
        # todo: 解析所有链接详细作者信息
        if self._type == "user":
            user_info = self.render_data.get(self._data_key, {}).get("user", {}).get("user", {})
            nickname = user_info.get("nickname")
            desc = user_info.get("nickname")
            ip_location = user_info.get("ipLocation")
            sec_uid = user_info.get("secUid")
            home = self.url_base.format(type="user", type_id=sec_uid)
            return AuthorInfo(nickname=nickname, desc=desc, ipLocation=ip_location, home=home)
        else:
            nickname = self.data_detail.get("authorInfo", {}).get("nickname", "")
            sec_uid = self.data_detail.get("authorInfo", {}).get("secUid")
            home = self.url_base.format(type="user", type_id=sec_uid)
            return AuthorInfo(nickname=nickname, home=home)

    def parse_info(self):
        """解析详细信息"""
        desc = self.data_detail.get("desc")

        return Info(url=self.parsed_url,
                    type=self._type,
                    desc=desc,
                    mixInfo=self.parse_mix_info())

    def parse_image(self):
        """开始解析图集"""
        images = self.data_detail.get("images")
        if not images:
            return ImageData()

        url_list = [img.get("urlList") for img in images]
        return ImageData(urlList=url_list)

    def parse_music(self):
        """开始解析背景音乐"""
        name = self.data_detail.get("music", {}).get("musicName")
        author = self.data_detail.get("music", {}).get("author")
        album = self.data_detail.get("music", {}).get("album")
        url = self.data_detail.get("music", {}).get("playUrl", {}).get("uri")

        return MusicData(name=name, author=author, album=album, url=url)

    def parse_video(self):
        """开始解析视频"""
        play_api = self.data_detail.get("video", {}).get("playApi")

        cover_url_list = self.data_detail.get("video", {}).get("coverUrlList")
        url = "https:{}".format(play_api) if play_api else ""

        return VideoData(coverUrlList=cover_url_list, url=url)

    def parse_user(self):
        """解析主页分享链接"""
        data = []

        for _data in self.render_data.get(self._data_key, {}).get("post", {}).get("data", []):
            self.data_detail = _data
            data.append(self.start_parse())
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
    txt = "长按复制此条消息，打开抖音搜索，查看TA的更多作品。 https://v.douyin.com/ihNJP1W/"

    tiktok: DouYinParser = DouYinParser()
    tiktok.parse(text)

    print(tiktok.data)
