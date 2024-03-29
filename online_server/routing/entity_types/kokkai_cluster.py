
from typing import TypedDict
from typing import List as typing_List  


class KokkaiCluster(TypedDict):
    title: str
    member_count: int
    short_keywords: typing_List[str]
    session: int


