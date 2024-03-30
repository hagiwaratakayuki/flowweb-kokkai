from fastapi import APIRouter, status
import json
import numpy as np
from typing import Optional


from .query.node import get_all_summary, get_linked_node as linked_node, get_node_keyword

from .query.cluster import get_clusters_by_node

from routing.return_models.node.overview import NodeOverView
from routing.return_models.node.overviews import NodeOverViews
from routing.return_models.node.nodefull import NodeFull
from routing.return_models.cluster.overview import ClusterOverView
from routing.return_models.cluster.overviews import ClusterOverViews

from typing import List
from db.proxy import Node
from app.error_hundling.status_exception import StatusException
from .router import get_routing_tuple
from data_types.position_data import PositionData
from typing import Optional

none_type = type(None)
router = APIRouter()


@router.get('/all_summary')
def all_as_vertex() -> list[NodeOverView]:  # type: ignore
    index = 0.0
    total_center: Optional[np.ndarray] = None
    entity_map = {}
    shape = [0, 0]
    is_first = True
    for e in get_all_summary.fetch():

        data: PositionData = json.loads(e['data'])['sentiment']

        position = np.array(data['position'])
        direction = np.array(data['direction'])
        if is_first == True:
            is_first = False
            shape[1] = direction.shape[0]

        if type(total_center) == none_type:
            total_center = position
        else:
            total_center += position
        entity_map[index] = {'entity': e,
                             'position': position, 'direction': direction}
        index += 1.0

    center: np.ndarray = total_center / index  # type: ignore

    totaldifference = 0.0
    intindex = int(index)
    shape[0] = intindex

    direction_vectors = np.zeros(shape=shape)
    positions_vectors = np.zeros(shape=shape)
    for i in range(0, intindex):

        direction_vectors[i] = entity_map[i]['direction']
        positions_vectors[i] = entity_map[i]['position']
    directions = np.dot(a=direction_vectors, b=center)  # type: ignore
    directions[directions >= 0.0] = 1.0
    directions[directions < 0.0] = -1.0
    positions = np.linalg.norm(positions_vectors, axis=1)
    max_norm = np.max(positions)
    positions *= directions
    positions /= max_norm

    ret = [NodeOverView(
        id=entity_map[i]['entity'].id or entity_map[i]['entity'].key.name,
        position=positions[i],
        **entity_map[i]['entity']
    )
        for i in range(0, intindex)]
    return ret


@router.get('/entity_all', response_model=NodeFull, response_model_exclude_none=True)
def get_entity_all(id: int) -> NodeFull:  # type: ignore
    entity = Node.get(id=id)

    if entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    link_to_ids = [{'id': link_to_id}
                   for link_to_id in entity.get('link_to', [])]
    link_to = [NodeOverView(id=e.id or e.key.name, **e)
               for e in Node.get_multi(link_to_ids) or []]  # type: ignore
    keywords = get_node_keyword.fetch(node_id=id)
    """
    cluster_entities, clusters_next = get_clusters_by_node.fetch(node_id=id)

    if cluster_entities == None:
        clusters = None
    else:
        clusters = [ClusterOverView(**e) for e in cluster_entities]
    """
    linked_from_entities, linked_from_next = linked_node.fetch(node_id=id)
    linked_from = [NodeOverView(id=e.id or e.key.name, **e)
                   for e in linked_from_entities or []]  # type: ignore

    return NodeFull(title=entity["title"],
                    body=entity["body"],
                    published=entity["published"],
                    author=entity["author"],
                    auther_id=entity["author_id"],
                    link_to=link_to,
                    clustres=[],
                    clustres_next="",
                    keywords=keywords,
                    linked_from=linked_from,
                    linked_from_next=linked_from_next
                    )


@router.get('/get_clusters', response_model=ClusterOverViews, response_model_exclude_none=True)
def get_clusters(id: str, cursor: Optional[str] = None) -> ClusterOverViews:
    cluster_entities, next_cursor = get_clusters_by_node.fetch(
        node_id=id, cursor=cursor)

    if cluster_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    clusters = [ClusterOverView(id=e.id, **e)
                for e in cluster_entities]  # type: ignore
    return ClusterOverViews(clusters=clusters, cursor=next_cursor)


@router.get('/get_linked_node', response_model=NodeOverViews, response_model_exclude_none=True)
def get_linked_node(id: str, cursor: str) -> NodeOverViews:
    node_entities, next_cursor = linked_node.fetch(node_id=id, cursor=cursor)
    if node_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    nodes = [NodeOverView(id=e.id, **e) for e in node_entities]  # type: ignore
    return NodeOverViews(nodes=nodes, cursor=next_cursor)


@router.get('/get_link_to', response_model=List[NodeOverViews], response_model_exclude_none=True)
def get_link_to(ids: list[str]) -> List[NodeOverView]:  # type: ignore
    node_entities = Node.get_multi(ids)
    if node_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    return [NodeOverView(id=e.id, **e) for e in node_entities]  # type: ignore


routing_tuple = get_routing_tuple(__file__, router)
