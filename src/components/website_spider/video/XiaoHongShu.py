
import json
import re

from urllib.parse import urlparse, urlunparse

from spider.base.spider import Spider


class XhsSpider(Spider):
    def __init__(self):
        super().__init__()
        self.data = dict()

    def get_data(self, _url):
        self.headers["accept"] = "text/html,application/xhtml+xml,application/xml;" \
                                 "q=0.9,image/webp,image/apng,*/*;" \
                                 "q=0.8,application/signed-exchange;v=b3;q=0.9"
        self.headers["Cookie"] = 'webBuild=2.8.6;' \
                                 'xsecappid=xhs-pc-web;' \
                                 'a1=188806ca1e3b8605b3otdl5uv4hhlcs5lj3izwgsz50000228326;' \
                                 'webId=c40eb2b2e6ac1211b35eeb1d1c07454e;' \
                                 'gid=yYYY8KS04S1KyYYY8KS0yVEkdqDYK82Dql9fqMu127h4x328x1SM2u888JJYqJK8iY802fqW;' \
                                 'gid.sign=Y35GIitj7ooTxCRX7xzaXZ07n08=;' \
                                 'web_session=030037a349a96c379e5254bb02234a5b4e817b;' \
                                 'cache_feeds=[];' \
                                 'websectiga=634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a;' \
                                 'sec_poison_id=9534efd6-4b78-4fc9-9eaa-942a68f178fc'
        html = self.get_html(_url)
        initial_state = html.xpath("/html/body/script[2]/text()")[0]
        tmp_regex = re.compile("(?<=\"note\":){.*}(?=,\"feed\")")
        initial_state_note = json.loads(tmp_regex.search(initial_state).group())
        self.data = initial_state_note.get("note", {})

    def get_images(self):
        image_list = self.data.get("imageList", [])
        images = [img.get("traceId") for img in image_list] if image_list else []
        parse_result = urlparse(self.data.get("imageList")[0].get("url"))
        images_base_url = urlunparse((parse_result.scheme, parse_result.netloc, "", "", "", ""))
        images = ["/".join([images_base_url, i]) for i in images]
        return images

    def get_title(self):
        return self.data.get("title")

    def get_video(self):
        video_path = self.data.get("video", {}).get("consumer", {}).get("originVideoKey")
        if not video_path:
            return
        video_stream = self.data.get("video", {}).get("media", {}).get("stream", {})
        video_master_pattern = video_stream.get("h264", []) or video_stream.get("h265", []) or video_stream.get("av1", [])
        video_master_url = video_master_pattern[0].get("masterUrl")
        parse_result = urlparse(video_master_url)
        video_base_url = urlunparse((parse_result.scheme, parse_result.netloc, "", "", "", ""))
        video = "/".join([video_base_url, video_path])
        return video


if __name__ == "__main__":
    url = "https://www.xiaohongshu.com/explore/647ab84100000000130130c7"
    base_url = [
        # images
        "https://sns-img-hw.xhscdn.com/",

        # video
        "http://sns-video-hw.xhscdn.com/",
        "http://sns-video-bd.xhscdn.com/",
        "http://sns-video-qc.xhscdn.com/",
        "http://sns-video-al.xhscdn.com/"


    ]

    xhs = XhsSpider()
    xhs.get_data(url)

    print(f"title: {xhs.get_title()}")
    print(f"video: {xhs.get_video()}")
    print(f"images: {xhs.get_images()}")

