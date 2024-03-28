
from typing import DefaultDict
from typing import Any as typing_Any  
from datetime import datetime as datetime_datetime  


class ClusterMember(DefaultDict):
    cluster_id:typing_Any
    text_id:str
    linked_count:int
    published:datetime_datetime
    position:float


