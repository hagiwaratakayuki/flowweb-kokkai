
from db.proxy import ClusterMember, Node
from typing import Optional


def fetch(cluster_id: int, cursor: Optional[str] = None, limit: int = 100):
    start_cursor = None
    if cursor != None:
        start_cursor = cursor.encode("utf-8")
    q = ClusterMember.query()
    q.add_filter("cluster_id", "=", cluster_id)
    q.order = ['-linked_count']
    q.projection = ["node_id"]
    itr = q.fetch(start_cursor=start_cursor, limit=limit)
    next_page_token = None
    if itr.next_page_token != None:
        next_page_token = itr.next_page_token.decode("utf-8")

    return Node.get_multi([{"id": e["node_id"]} for e in itr]), next_page_token


def indexer():
    fetch(1)
