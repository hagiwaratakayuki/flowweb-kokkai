from routing.return_models.cluster.overview import ClusterOverView
from routing.return_models.node.overview import NodeOverView
from db.proxy import Node
from util.create_type import create_pydantec_model


import datetime
from typing import Literal, Union


NodeFull = create_pydantec_model(name_template='NodeFull', base=Node, extend_map={
    'keywords': {
        'type': list[str],
        'default': []
    },
    'clustres': {
        'type': Union[list[ClusterOverView], None],
        'default': None
    },
    'clustres_next': {
        'type': Union[None,  str],
        'default': None
    },
    'link_to': {
        'type': Union[list[NodeOverView], None],
        'default': None
    },
    'linked_from': {
        'type': Union[list[NodeOverView], None],
        'default': None
    },
    'linked_from_next': {
        'type': Union[Literal[False], str],
        'default': False
    }
})

"""

class NodeFull(BaseModel):
    title: str = ''
    body: str = ''
    published: datetime.datetime
    author: str = ''
    auther_id: str = ''
    keywords: list[str] = []
    clustres: Union[list[ClusterOverView], None] = None  # type: ignore
    clustres_next: Union[None,  str] = None
    link_to: Union[list[NodeOverView], None] = None  # type: ignore
    linked_from: Union[list[NodeOverView], None] = None  # type: ignore
    linked_from_next: Union[Literal[False], str] = False
"""
