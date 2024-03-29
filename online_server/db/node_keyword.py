from .model import Model
from typing import List
from datetime import datetime


class NodeKeyword(Model):
    keyword: str
    published: datetime
    node_id: str
    linked_count: int
    weight: float
    published_list: List[str]
