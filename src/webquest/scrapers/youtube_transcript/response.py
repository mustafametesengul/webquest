from pydantic import BaseModel


class YouTubeTranscriptResponse(BaseModel):
    """
    Represents the extracted transcript of a YouTube video.
    """

    transcript: str
