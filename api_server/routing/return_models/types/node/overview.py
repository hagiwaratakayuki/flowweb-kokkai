
# This is auto generated. see tools/api_sever/create_responsetype.py
from typing import Any
from pydantic import BaseModel
from typing import Optional as typing_Optional, List as typing_List, Union as typing_Union
from datetime import datetime as datetime_datetime


class NodeOverview(BaseModel):
    id: Any
    data: str
    author: str
    author_id: str
    link_to: typing_Optional[typing_List[str]]
    published: datetime_datetime
    title: str
    published_list: typing_Optional[typing_List[str]]
    keywords: typing_List[str]
    house: str
    session: int
    position: typing_Union[str, float]
