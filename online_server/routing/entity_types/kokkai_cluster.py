
from typing import DefaultDict
from typing import List as typing_List  


class KokkaiCluster(DefaultDict):
    title:str
    member_count:int
    short_keywords:typing_List[str]
    session:int


