from enum import Enum
from typing import List, Generic, TypeVar, Optional

from pydantic import BaseModel, Field, validator
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


class MediaType(str, Enum):
    note = 'image'
    video = 'video'


class MixInfo(BaseModel):
    """合集相关信息"""
    is_collection: bool = Field(default=..., alias="isCollection", description="是否为合集")
    mix_id: str = Field(default='', alias="mixId", description="合集id")
    mix_name: str = Field(default='', alias="mixName", description="合集名字")
    desc: str = Field(default='', alias="desc", description="合集描述")
    current_episode: int = Field(default=0, alias="currentEpisode", description="合集当前序集")
    total_episode: int = Field(default=0, alias="totalEpisode", description="合集总序集")
    cover_url_list: list = Field(default=[], alias="coverUrlList", description="合集封面链接")


class Info(BaseModel):
    origin_url: str = Field(default='', alias="originUrl", description="视频网址")
    type: MediaType = Field(default='', alias="type", description="媒体类型: 视频, 图片...")
    author: str = Field(default='', alias="author", description="视频作者昵称")
    desc: str = Field(default='', alias="desc", description="视频描述")
    mix_info: MixInfo = Field(default=..., alias="mixInfo", description="合集信息")

    @validator('type', always=True)
    def check_type(cls, v, values):
        # if v is not None and values['data'] is not None:
        #     raise ValueError('must not provide both data and error')
        if v not in ['image', 'video']:
            raise ValueError(f'<{v}> must be note or video')
        return v


class MusicData(BaseModel):
    name: str = Field(default='', alias="name", description="音乐名称")
    author: str = Field(default='', alias="author", description="音乐作者")
    album: str = Field(default='', alias="album", description="音乐专辑")
    url: str = Field(default='', alias="url", description="音乐链接")


class ImageData(BaseModel):
    url_list: list = Field(default=[], alias="urlList", description="音乐链接列表")


class VideoData(BaseModel):
    data_size: int = Field(default=0, alias="dataSize", description="视频大小(Byte)")
    url_list: list = Field(default=[], alias="urlList", description="视频链接")
    cover_url_list: list = Field(default=[], alias="coverUrlList", description="视频封面链接")
    url: str = Field(default='', alias="url", description="视频链接")


class MediaData(BaseModel):
    info: Info = Field()
    music: MusicData = Field()
    images: ImageData = Field()
    video: VideoData = Field()


class AuthorInfo(BaseModel):
    """作者相关信息"""
    nickname: str = Field(default='', alias="nickname", description="视频作者昵称")
    home: str = Field(default='', alias="home", description="作者主页链接")
    signature: str = Field(default='', alias="signature", description="作者描述")
    avatar_url_list: list = Field(default=[], alias="avatarUrlList", description="头像")
    # ip_location: str = Field(default='', alias="ipLocation", description="作者ip地址")
    country: str = Field(default='', alias="country", description="作者所在国家")
    province: str = Field(default='', alias="province", description="作者所在省份")
    city: str = Field(default='', alias="city", description="作者所在城市")
    school_name: str = Field(default='', alias="schoolName", description="作者所在学校")
    cover_image_info: list = Field(default=[], alias="coverImageInfo", description="主页封面信息")
    tags: List[str] = Field(default=[], alias="tags", description="标签")
    fields: List[str] = Field(default=[], alias="fields", description="相关属性")
    suggestion: str = Field(default="", alias="suggestion", description="相关建议")


class ParsedData(BaseModel):
    author_info: AuthorInfo = Field(default=..., alias="authorInfo", description="视频作者")
    data: List[MediaData] = Field(default=[],  alias="data", description="视频解析数据")


class _MediaData(GenericModel, Generic[DataT]):
    info: Optional[Info]

    data: Optional[DataT]
    # error: Optional[ResponseError]

    @validator('data', always=True)
    def check_consistency(cls, v, values):
        # if v is not None and values['data'] is not None:
        #     raise ValueError('must not provide both data and error')
        if v is None and values.get('data') is None:
            raise ValueError('must provide data or error')
        return v


if __name__ == "__main__":
    img = ImageData(urlList=['a', 's'])
    print(img.json())
