
# This is auto generated. see tools/api_sever/create_responsetype.py 
from typing import Any
from pydantic import BaseModel
from typing import List as typing_List  



class ClusterOverview(BaseModel):
    id:Any
    title: str
    member_count: int
    keywords: typing_List[str]
    weight: float
    total_weight: float
    session: int


