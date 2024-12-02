from typing import Any
from pydantic import BaseModel
from typing import List as typing_List

from routing.return_models.types.node.overviews import NodeOverviews


class ClusterData(BaseModel):
    id: Any
    keywords: list[str]
    members: NodeOverviews
    member_count: int
