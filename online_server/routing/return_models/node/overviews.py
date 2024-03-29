from pydantic import BaseModel
from .overview import NodeOverView
from ..with_cursor import WithCursor


class NodeOverViews(BaseModel, WithCursor):
    nodes: list[NodeOverView]  # type: ignore
