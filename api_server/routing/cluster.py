import asyncio
from fastapi import APIRouter, status

from db.proxy import Cluster
from db.proxy import Node
from typing import Any, List
from .query.cluster import get_cluster_by_keyword, get_cluster_member, get_cluster_member_by_publishedrange
from application.error_hundling.status_exception import StatusException
from pydantic import BaseModel
from routing.return_models.types.node.overview import NodeOverview
from routing.return_models.types.node.overviews import NodeOverviews
from .router import get_routing_tuple
from .return_models.types.cluster.data import ClusterData
from typing import Optional
router = APIRouter()
from .util.entity2responsetype import entity2responsetype, entity2responsetype_list


class ClusterFull(BaseModel):
    id: Any
    keywords: list[str]
    members_list: Optional[list[NodeOverview]]  # type: ignore
    members_list_next: Optional[str]
    member_count: int


@router.get('/data', response_model=ClusterFull, response_model_exclude_none=True)
async def get_entity_all(id: int) -> ClusterData:

    cluster, [members_entities, members_list_next] = await asyncio.gather(Cluster.get_async(id=id), get_cluster_member.fetch(
        cluster_id=id))
    if cluster == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)

    members_list: Optional[list] = None
    if members_entities != None:
        members_list = entity2responsetype_list(
            NodeOverview, entities=members_entities)
    return dict(
        id=cluster.key.id_or_name,
        keywords=cluster.get("keywords", []),
        member_count=cluster["memebr_count"],
        members_list=members_list,
        members_list_next=members_list_next)


@router.get('/members', response_model=NodeOverviews, response_model_exclude_none=True)
def get_members(id: int, cursor: Optional[str] = None) -> NodeOverviews:
    members_entities, members_list_next = get_cluster_member.fetch(
        cluster_id=id, cursor=cursor)
    if members_entities == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    nodes = [NodeOverview(**mem) for mem in members_entities]
    return NodeOverviews(nodes=nodes, cursor=members_list_next)


@router.get('/members_by_publishedate', response_model=List[NodeOverview], response_model_exclude_none=True)
def get_members_by_publishedate(
        eid: str,
        start_year: int,
        start_month: int,
        start_date: int,
        end_year: int,
        end_month: int,
        end_date: int,

) -> List[NodeOverview]:  # type: ignore

    members = get_cluster_member_by_publishedrange.fetch(
        cluster_id=eid,
        start_year=start_year,
        start_month=start_month,
        start_date=start_date,
        end_year=end_year,
        end_month=end_month,
        end_date=end_date,
    )
    if members == None:
        raise StatusException(status=status.HTTP_400_BAD_REQUEST)
    return [NodeOverview(id=mem.id, **mem) for mem in members]  # type: ignore


routing_tuple = get_routing_tuple(__file__, router)
