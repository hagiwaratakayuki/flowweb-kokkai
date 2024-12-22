import logging
from fastapi import APIRouter, status
from typing import Literal, Optional, Union

from routing.components.node.adjast_to_view import adjast_to_view


from .query.node import get_all_summary, get_link_from_node as linked_node

from .query.cluster import get_clusters_by_node

from routing.return_models.types.node.overview import NodeOverview
from routing.return_models.types.node.overviews import NodeOverviews
from routing.return_models.types.cluster.overview import ClusterOverview
from routing.return_models.types.cluster.overviews import ClusterOverviews

from typing import List, Optional

from db.proxy import Node
from application.error_hundling.status_exception import StatusException
from .router import get_routing_tuple


none_type = type(None)
router = APIRouter()


class NodeFull(NodeOverview):
    body: str
    clustres: Optional[list[ClusterOverview]] = None
    clustres_next: Optional[str] = None
    link_to: Optional[list[NodeOverview]] = None
    linked_from: Optional[list[NodeOverview]] = None
    linked_from_next: Union[Literal[False], str] = False


@router.get('/all_summary')
async def all_as_vertex():  # type: ignore
    itr = await get_all_summary.fetch()
    return adjast_to_view(itr)


@router.get('/entity_all', response_model=NodeFull, response_model_exclude_none=True)
def get_entity_all(id: int) -> NodeFull:  # type: ignore
    entity = Node.get(id=id)

    if entity == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    link_to_ids = [{'id': link_to_id}
                   for link_to_id in entity.get('link_to', [])]
    link_to = [NodeOverview(id=e.id or e.key.name, **e)
               for e in Node.get_multi(link_to_ids) or []]  # type: ignore
    keywords = entity['keywords']
    linked_from_entities, linked_from_next = linked_node.fetch(node_id=id)
    linked_from = [NodeOverview(id=e.id or e.key.name, **e)
                   for e in linked_from_entities or []]  # type: ignore

    return NodeFull(title=entity["title"],
                    body=entity["body"],
                    published=entity["published"],
                    author=entity["author"],
                    author_id=entity["author_id"],
                    link_to=link_to,
                    clustres=[],
                    clustres_next="",
                    keywords=keywords,
                    linked_from=linked_from,
                    linked_from_next=linked_from_next
                    )


@router.get('/get_clusters', response_model=ClusterOverviews, response_model_exclude_none=True)
def get_clusters(id: str, cursor: Optional[str] = None) -> ClusterOverviews:
    cluster_entities, next_cursor = get_clusters_by_node.fetch(
        node_id=id, cursor=cursor)

    if cluster_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    clusters = [ClusterOverview(id=e.id, **e)
                for e in cluster_entities]  # type: ignore
    return ClusterOverviews(overviews=clusters, cursor=next_cursor)


@router.get('/get_linked_node', response_model=NodeOverviews, response_model_exclude_none=True)
def get_linked_node(id: str, cursor: str) -> NodeOverviews:
    node_entities, next_cursor = linked_node.fetch(node_id=id, cursor=cursor)
    if node_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    nodes = [NodeOverview(id=e.id, **e) for e in node_entities]  # type: ignore
    return NodeOverviews(nodes=nodes, cursor=next_cursor)


@router.get('/get_link_to', response_model=List[NodeOverviews], response_model_exclude_none=True)
def get_link_to(ids: list[str]) -> List[NodeOverview]:  # type: ignore
    node_entities = Node.get_multi(ids)
    if node_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    return [NodeOverview(id=e.id, **e) for e in node_entities]  # type: ignore


routing_tuple = get_routing_tuple(__file__, router)
