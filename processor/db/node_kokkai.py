import json
import math
from datetime import datetime
from .node import Node


class NodeKokkai(Node):
    house: str
    session: int
    comittie: str
    group: str
