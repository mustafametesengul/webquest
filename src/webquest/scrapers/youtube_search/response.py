from pydantic import BaseModel


class Video(BaseModel):
    """
    Represents a YouTube video.

    Attributes:
        id: The unique identifier of the video.
        url: The URL of the video.
        title: The title of the video.
        description: The description of the video.
        published_at: The publication date of the video.
        views: The view count of the video.
        channel_id: The ID of the channel that uploaded the video.
        channel_url: The URL of the channel.
        channel_name: The name of the channel.
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

    Attributes:
        id: The unique identifier of the channel.
        url: The URL of the channel.
        name: The name of the channel.
        description: The description of the channel.
        subscribers: The subscriber count of the channel.
    """

    id: str
    url: str
    name: str
    description: str | None
    subscribers: str


class Post(BaseModel):
    """
    Represents a YouTube community post.

    Attributes:
        id: The unique identifier of the post.
        url: The URL of the post.
        content: The content of the post.
        published_at: The publication date of the post.
        channel_id: The ID of the channel that created the post.
        channel_url: The URL of the channel.
        channel_name: The name of the channel.
        comments: The comment count of the post.
        likes: The like count of the post.
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

    Attributes:
        id: The unique identifier of the short.
        url: The URL of the short.
        title: The title of the short.
        views: The view count of the short.
    """

    id: str
    url: str
    title: str
    views: str


class YouTubeSearchResponse(BaseModel):
    """
    Represents the response from a YouTube search.

    Attributes:
        videos: A list of videos found.
        channels: A list of channels found.
        posts: A list of community posts found.
        shorts: A list of shorts found.
    """

    videos: list[Video]
    channels: list[Channel]
    posts: list[Post]
    shorts: list[Short]
