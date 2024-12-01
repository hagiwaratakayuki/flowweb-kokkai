from pydantic import BaseModel
from .overview import ClusterOverview
from typing import List, Optional


class ClusterOverviews(BaseModel):
    overviews: List[ClusterOverview]
    cursor: Optional[str]
