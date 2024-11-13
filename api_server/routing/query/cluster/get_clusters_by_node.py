from db.proxy import Cluster, ClusterMember
from typing import Optional
import asyncio
from routing.query.pattern import cursorfetch


async def fetch(node_id: str, cursor: Optional[str] = None, limit: int = 10):
    await asyncio.sleep(0)
    q = ClusterMember.query()
    q.add_filter("node_id", "=", node_id)
    q.order = ['-linked_count']
    q.projection = ["cluster_id"]
    itr, next_token = cursorfetch.fetch(query=q, cursor=cursor, limit=limit)

    return Cluster.get_multi([{"id": e["cluster_id"]} for e in itr]), next_token


def indexer():
    asyncio.run(fetch(0))
