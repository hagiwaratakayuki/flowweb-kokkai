from typing import Any, Optional
from pydantic import BaseModel
from ..cluster.data import ClusterData


class KokkaiClusterLink(BaseModel):
    id: Any
    issue: Any


class KokkaiClusterData(ClusterData):
    before_cluster: Optional[KokkaiClusterLink]
    after_cluster: Optional[KokkaiClusterLink]
