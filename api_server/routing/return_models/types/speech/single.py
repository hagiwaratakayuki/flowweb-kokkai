
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel
from typing import Optional as typing_Optional  



class SpeechSingle(BaseModel):
    id:Any
    speaker: str
    speaker_id: str
    response_to: typing_Optional[str]
    response_from: typing_Optional[str]
    discussion_id: str
    url: str
    order: int
    session: int
    issue: str
    house: str
    body: str


