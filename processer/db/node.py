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
    session: int

    def __init__(self, *args, **kwargs) -> None:

        super(Node, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "title", )}, *args, **kwargs)

    def setProperty(self,  session, data, linked_to: list[str], linked_count: int, published: datetime, author: str, author_id: str):
        self.link_to = linked_to
        self.session = session
        if type(published) == str:
            published = datetime.fromisoformat()

        self.published = published
        self.data = json.dumps(data)
        self.linked_count = linked_count
        self.author_id = author_id
        if linked_count == 0:
            weight = 0.0
        else:
            weight = math.log(linked_count) * (float(published.year) +
                                               float(published.month) / 100.0 + float(published.day) / 10000.0)

        self.weight = weight
