import json
import math
from datetime import datetime
from .node import Node


class NodeKokkai(Node):

    session: int

    def __init__(self, *args, **kwargs) -> None:

        super(Node, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "title", )}, *args, **kwargs)

    def setProperty(self, dto, data, title, link_to: list[str], linked_count: int, published: datetime, author: str, author_id: str):
        return super().setProperty(data, title, link_to, linked_count, published, author, author_id)
