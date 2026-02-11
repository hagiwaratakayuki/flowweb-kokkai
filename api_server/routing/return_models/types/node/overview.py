
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel
from typing import Optional as typing_Optional , List as typing_List , Union as typing_Union  
from datetime import datetime as datetime_datetime  



class NodeOverview(BaseModel):
    id:Any
    author: str
    author_id: str
    link_to: typing_Optional[typing_List[str]]
    linked_count: int
    published: datetime_datetime
    title: str
    published_list: typing_Optional[typing_List[str]]
    keywords: typing_List[str]
    is_apex: bool
    house: str
    session: int
    comittie: str
    group: str
    position: typing_Union[str, float]


