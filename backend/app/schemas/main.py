from pydantic import BaseModel

class AskRequest(BaseModel):
    question: str

class Train_YoutubeRequest(BaseModel):
    youtube_link: str
