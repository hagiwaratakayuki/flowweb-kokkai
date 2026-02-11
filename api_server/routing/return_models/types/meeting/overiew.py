
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel




class MeetingOveriew(BaseModel):
    id:Any
    session: int
    issue: int
    name: str
    house: str


