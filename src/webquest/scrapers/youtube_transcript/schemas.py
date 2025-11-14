from pydantic import BaseModel


class Request(BaseModel):
    video_id: str


class Response(BaseModel):
    transcript: str
