
from .basetype import BaseType
from typing import Any as typing_Any  
from datetime import datetime as datetime_datetime  


class ClusterMember(BaseType):
    cluster_id: typing_Any
    node_id: str
    linked_count: int
    published: datetime_datetime
    position: float
    weight: float


