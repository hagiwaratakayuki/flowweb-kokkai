
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel




class SpeakerSingle(BaseModel):
    id:Any
    name: str
    group: str
    position: str
    session: int
    role: str
    house: str
    comittie: str


