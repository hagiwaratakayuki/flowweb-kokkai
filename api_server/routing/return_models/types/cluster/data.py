

from typing import Any, Optional, List
from pydantic import BaseModel


from routing.return_models.types.node.overviews import NodeOverviews


class ClusterLink(BaseModel):
    id: Any
    keywords: Optional[List[str]]


class ClusterLinks(BaseModel):
    clusters: Optional[List[ClusterLink]]


class ClusterData(BaseModel):
    id: Any
    keywords: list[str]
    members: NodeOverviews
    member_count: int
    links: List[ClusterLink]
