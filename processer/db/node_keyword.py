from .model import Model
from datetime import datetime


class NodeKeyword(Model):
    keyword: str
    published: datetime
    text_id: str
    linked_count: int
