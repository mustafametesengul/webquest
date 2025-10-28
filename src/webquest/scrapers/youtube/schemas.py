from datetime import datetime

from pydantic import BaseModel


class Video(BaseModel):
    id: str
    url: str
    title: str
    image_url: str
    published_at: datetime
    views: int
    length_seconds: int
    channel_id: str
    channel_url: str
    channel_name: str
    channel_image_url: str


class Channel(BaseModel):
    id: str
    url: str
    name: str
    description: str
    image_url: str
    subscribers: int


class ChannelVideosPage(BaseModel):
    videos: list[Video]


class Post(BaseModel):
    id: str
    url: str
    content: str
    published_at: datetime
    channel_id: str
    channel_url: str
    channel_name: str
    channel_image_url: str
    comments: int
    likes: int


class Short(BaseModel):
    id: str
    url: str
    title: str
    image_url: str
    views: int


class SearchResult(BaseModel):
    videos: list[Video]
    channels: list[Channel]
    posts: list[Post]
    shorts: list[Short]


class TranscriptRequest(BaseModel):
    video_id: str


class TranscriptResult(BaseModel):
    transcript: str
