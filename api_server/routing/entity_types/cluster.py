
from .basetype import BaseType
from typing import List as typing_List  


class Cluster(BaseType):
    title: str
    member_count: int
    keywords: typing_List[str]
    weight: float
    total_weight: float


