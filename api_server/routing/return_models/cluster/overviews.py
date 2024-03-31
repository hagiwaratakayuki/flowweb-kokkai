from pydantic import BaseModel
from .overview import ClusterOverview
from typing import Optional


class ClusterOverviews(BaseModel):
    # clusters: list[ClusterOverview]
    cursor: Optional[str]
