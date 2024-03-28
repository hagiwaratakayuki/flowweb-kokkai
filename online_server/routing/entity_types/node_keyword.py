
from typing import DefaultDict
from datetime import datetime as datetime_datetime  
from typing import List as typing_List  


class NodeKeyword(DefaultDict):
    keyword:str
    published:datetime_datetime
    text_id:str
    linked_count:int
    weight:float
    published_list:typing_List[str]


