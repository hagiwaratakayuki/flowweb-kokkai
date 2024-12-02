
from db.proxy import ClusterMember, Node
from typing import Optional
from ..pattern import cursorfetch


def fetch(cluster_id: int, cursor: Optional[str] = None, limit: int = 100):
    start_cursor = None
    if cursor != None:
        start_cursor = cursor.encode("utf-8")
    q = ClusterMember.query()
    q.add_filter("cluster_id", "=", cluster_id)
    q.order = ['-linked_count']
    q.projection = ["node_id"]
    itr, next_page_token = cursorfetch.fetch(
        query=q, cursor=cursor, limit=limit)

    return Node.get_multi([{"id": e["node_id"]} for e in itr]), next_page_token


def indexer():
    fetch(1)
