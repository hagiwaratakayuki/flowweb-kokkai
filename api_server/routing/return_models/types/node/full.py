from routing.return_models.types.cluster.overview import ClusterOverview
from routing.return_models.types.node.overview import NodeOverview


import datetime
from typing import Literal, Union


class NodeFull(NodeOverview):
    body: str
    clustres: Union[list[ClusterOverview], None] = None  # type: ignore
    clustres_next: Union[None,  str] = None
    link_to: Union[list[NodeOverview], None] = None  # type: ignore
    linked_from: Union[list[NodeOverview], None] = None  # type: ignore
    linked_from_next: Union[Literal[False], str] = False
