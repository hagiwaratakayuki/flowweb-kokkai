from typing import Any, List, Optional
from pydantic import BaseModel
from ..cluster.data import ClusterData


class KokkaiClusterLink(BaseModel):
    id: Any
    issue: Any
    keywords: List[str]


class KokkaiClusterData(ClusterData):
    before_cluster: Optional[KokkaiClusterLink]
    after_cluster: Optional[KokkaiClusterLink]
