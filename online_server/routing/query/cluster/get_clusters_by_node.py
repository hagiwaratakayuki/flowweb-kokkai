from db.proxy import Cluster, ClusterMember
from typing import Optional


def fetch(node_id: str, cursor: Optional[str] = None, limit: int = 10):
    start_cursor = None
    if cursor != None:
        start_cursor = cursor.encode('utf-8')
    q = ClusterMember.query()
    q.add_filter("node_id", "=", node_id)
    q.order = ['-linked_count']
    q.projection = ["cluster_id"]
    itr = q.fetch(limit=limit, start_cursor=start_cursor)
    next_token = None
    if itr.next_page_token != None:
        next_token = itr.next_page_token.decode('utf-8')

    return Cluster.get_multi([{"id": e["cluster_id"]} for e in itr]), next_token
