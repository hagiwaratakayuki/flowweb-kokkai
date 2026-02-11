
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel




class SpeechOverview(BaseModel):
    id:Any
    title: str
    meeting_id: str
    meeting: str
    speaker: str
    speaker_id: str


