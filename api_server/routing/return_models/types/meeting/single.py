
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel
from typing import List as typing_List , Dict as typing_Dict , Any as typing_Any  



class MeetingSingle(BaseModel):
    id:Any
    session: int
    issue: int
    name: str
    url: str
    pdf: str
    header_text: str
    moderators: typing_List[typing_Dict[str, typing_Any]]
    moderator_ids: typing_List[str]
    keywords: typing_List[str]
    house: str


