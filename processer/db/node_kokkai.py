import json
import math
from datetime import datetime
from .node import Node


class NodeKokkai(Node):

    session: int

    def __init__(self, *args, **kwargs) -> None:

        super(Node, self).__init__(entity_options={
            "exclude_from_indexes": ("data", "title", )}, *args, **kwargs)
