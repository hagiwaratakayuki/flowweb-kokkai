
# This is auto generated. see tools/api_sever/create_responsetype.py 

from pydantic import BaseModel
from typing import Optional as typing_Optional , List as typing_List , Union as typing_Union  
from datetime import datetime as datetime_datetime  



class NodeOverview(BaseModel):
    data: str
    author: str
    author_id: str
    link_to: typing_Optional[typing_List[str]]
    linked_count: int
    published: datetime_datetime
    weight: float
    title: str
    published_list: typing_List[str]
    hash: str
    session: int
    position: typing_Union[str, int, NoneType]


