
import os

from common.utils.utils import load_yaml

BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


class Xpath(object):
    title = ''
    chapter = ''


class Configuration:
    script_path = r"C:\Users\fujun\Desktop\CodeHub\StorySpider\scripts"
    config_path = r"C:\Users\fujun\Desktop\CodeHub\StorySpider\config"
    x_bogus_js = "X-Bogus.js"
    requests_config_filename = "Requests.yaml"
    dy_x_bogus_js = os.sep.join([script_path, x_bogus_js])
    requests_config_file = os.sep.join([config_path, requests_config_filename])


requests_config = load_yaml(Configuration.requests_config_file)


class DYApiConfig:
    aid: int = requests_config.get("douyin", {}).get("aid")

    index_url: str = requests_config.get("douyin", {}).get("indexUrl")
    url_base: str = requests_config.get("douyin", {}).get("baseUrl")
    user_data_api: str = requests_config.get("douyin", {}).get("userDataApi")
    video_data_api: str = requests_config.get("douyin", {}).get("videoDataApi")
    user_profile_api: str = requests_config.get("douyin", {}).get("userProfileApi")

    cookies: str = requests_config.get("douyin", {}).get("Cookies")


if __name__ == '__main__':
    print(DYApiConfig.aid, type(DYApiConfig.aid))
