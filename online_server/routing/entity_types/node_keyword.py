
from .basetype import BaseType
from datetime import datetime as datetime_datetime  
from typing import List as typing_List  


class NodeKeyword(BaseType):
    keyword: str
    published: datetime_datetime
    node_id: str
    linked_count: int
    weight: float
    published_list: typing_List[str]


