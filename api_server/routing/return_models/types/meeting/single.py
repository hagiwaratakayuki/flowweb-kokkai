
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel
from typing import List as typing_List  



class MeetingSingle(BaseModel):
    id:Any
    session: int
    issue: int
    name: str
    url: str
    pdf: str
    header_text: str
    moderators: dict
    moderator_ids: typing_List[str]
    keywords: typing_List[str]
    house: str


