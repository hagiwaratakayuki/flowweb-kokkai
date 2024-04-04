
# This is auto generated. see tools/api_sever/create_responsetype.py 

from pydantic import BaseModel




class SpeechSimple(BaseModel):
    meeting_id: str
    meeting: str
    speaker: str
    speaker_id: str
    response_to: str
    response_from: str
    discussion_id: str
    url: str
    order: int
    session: int
    issue: str
    house: str
    body: str


