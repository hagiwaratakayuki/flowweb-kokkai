
import asyncio
from collections import deque
from enum import member
from platform import node
from db.proxy import ClusterMember, Node
from typing import Optional
from ..pattern import cursorfetch


async def fetch(cluster_id: int, cursor: Optional[str] = None, limit: int = 100):
    asyncio.sleep(0)
    q = ClusterMember.query()
    q.add_filter("cluster_id", "=", cluster_id)
    q.order = ['-linked_count']
    q.projection = ["node_id", "position"]
    itr, next_page_token = cursorfetch.fetch(
        query=q, cursor=cursor, limit=limit)
    member_enities = deque(itr)
    node_map = {node_entity.key.id_or_name: node_entity for node_entity in Node.get_multi(
        [{"id": e["node_id"]} for e in member_enities])}
    node_members = [(node_map[member_entity['node_id']], member_entity, )
                    for member_entity in member_enities]
    return node_members, next_page_token


def indexer():
    fetch(1)
