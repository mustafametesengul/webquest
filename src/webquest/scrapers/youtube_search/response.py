from pydantic import BaseModel


class Video(BaseModel):
    """
    Represents a YouTube video.
    """

    id: str
    url: str
    title: str
    description: str
    published_at: str
    views: str
    channel_id: str
    channel_url: str
    channel_name: str


class Channel(BaseModel):
    """
    Represents a YouTube channel.
    """

    id: str
    url: str
    name: str
    description: str | None
    subscribers: str


class Post(BaseModel):
    """
    Represents a YouTube community post.
    """

    id: str
    url: str
    content: str
    published_at: str
    channel_id: str
    channel_url: str
    channel_name: str
    comments: str
    likes: str


class Short(BaseModel):
    """
    Represents a YouTube Short.
    """

    id: str
    url: str
    title: str
    views: str


class YouTubeSearchResponse(BaseModel):
    """
    Represents the response from a YouTube search.
    """

    videos: list[Video]
    channels: list[Channel]
    posts: list[Post]
    shorts: list[Short]
