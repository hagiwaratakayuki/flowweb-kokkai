from db.kokkai_cluster_link import KokkaiClusterLink
from db.kokkai_cluster import KokkaiCluster
import asyncio

from google.cloud.datastore.query import PropertyFilter


async def fetch(id):
    await asyncio.sleep(0)
    q = KokkaiClusterLink.query()
    q.add_filter(filter=PropertyFilter("from_cluster", '=', id))
    ids = [{'id': r['to_cluster']} for r in q.fetch()]
    if len(ids) == 0:
        return None
    ret = await KokkaiCluster.get_multi_async(ids)
    return ret[0]
