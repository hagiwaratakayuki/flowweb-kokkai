from .model import Model
from typing import Union
import json
import math
from datetime import datetime


class Node(Model):
    data: str
    author: str = ''
    author_id: str = ''
    link_to: Union[list[str], None]
    linked_count: int
    published: datetime
    weight: float

    def __init__(self, *args, **kwargs) -> None:

        super(Node, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "body", "title", )}, *args, **kwargs)

    def setProperty(self,  data, linked_to: list[str], linked_count: int, published: datetime, author: str, author_id: str):
        self.link_to = linked_to
        if type(published) == str:
            published = datetime.fromisoformat()

        self.published = published
        self.data = json.dumps(data)
        self.linked_count = linked_count
        if linked_count == 0:
            weight = 0.0
        else:
            weight = math.log(linked_count) * (float(published.year) +
                                               float(published.month) / 100.0 + float(published.day) / 10000.0)

        self.weight = weight
