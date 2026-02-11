from typing import Any, List, Optional

from pydantic import BaseModel
from ..cluster.data import ClusterData


class KokkaiClusterLink(BaseModel):
    id: Any
    session: Any
    keywords: List[str]


class KokkaiClusterData(ClusterData):
    session: Any
    before_cluster: Optional[KokkaiClusterLink]
    after_cluster: Optional[KokkaiClusterLink]
