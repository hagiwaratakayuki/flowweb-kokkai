
from .basetype import BaseType
from typing import List as typing_List  


class KokkaiCluster(BaseType):
    title: str
    member_count: int
    short_keywords: typing_List[str]
    session: int


