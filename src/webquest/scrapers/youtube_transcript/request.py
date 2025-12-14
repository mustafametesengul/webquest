from pydantic import BaseModel


class YouTubeTranscriptRequest(BaseModel):
    """
    Represents a request to extract the transcript of a YouTube video.
    """

    video_id: str
