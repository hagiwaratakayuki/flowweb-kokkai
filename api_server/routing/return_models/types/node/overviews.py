from pydantic import BaseModel
from .overview import NodeOverview
from ...with_cursor import WithCursor


class NodeOverviews(BaseModel, WithCursor):
    nodes: list[NodeOverview]  # type: ignore
