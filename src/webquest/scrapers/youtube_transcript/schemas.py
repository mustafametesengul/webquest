from pydantic import BaseModel


class Request(BaseModel):
    video_id: str


class Result(BaseModel):
    transcript: str
