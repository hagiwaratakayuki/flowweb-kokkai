
from typing import DefaultDict
from typing import Any as typing_Any  
from datetime import datetime as datetime_datetime  


class Edge(DefaultDict):
    linked_from:typing_Any
    link_to:typing_Any
    linked_count:int
    published:datetime_datetime


