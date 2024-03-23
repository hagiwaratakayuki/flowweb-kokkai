from pydantic import BaseModel
from .overview import NodeOverView
from typing import Literal


class NodeOverViews(BaseModel):
    texts: list[NodeOverView]
    cursor: str | Literal[False]
