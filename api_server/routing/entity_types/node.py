
from .basetype import BaseType
from typing import Optional as typing_Optional , List as typing_List  
from datetime import datetime as datetime_datetime  


class Node(BaseType):
    data: str
    author: str
    author_id: str
    link_to: typing_Optional[typing_List[str]]
    linked_count: int
    published: datetime_datetime
    weight: float
    title: str
    published_list: typing_List[str]
    keywords: typing_List[str]
    hash: str


