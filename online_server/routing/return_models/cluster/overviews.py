from pydantic import BaseModel
from .overview import ClusterOverView
from typing import Optional


class ClusterOverViews(BaseModel):
    clusters: list[ClusterOverView]  # type: ignore
    cursor: Optional[str]
