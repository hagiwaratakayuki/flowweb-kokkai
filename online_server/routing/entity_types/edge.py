
from typing import TypedDict
from typing import Any as typing_Any  
from datetime import datetime as datetime_datetime  


class Edge(TypedDict):
    linked_from: typing_Any
    link_to: typing_Any
    linked_count: int
    published: datetime_datetime


