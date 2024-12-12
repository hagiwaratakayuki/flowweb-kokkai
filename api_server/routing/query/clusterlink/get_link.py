import asyncio
from db.cluster_link import ClusterLink
from db.proxy import Cluster
from google.cloud.datastore.query import PropertyFilter


async def fetch(cluster_id):
    await asyncio.sleep(0)
    itr = ClusterLink.query().add_filter(filter=PropertyFilter(
        "link_start", '=', cluster_id)).fetch()
    entity_to_link_count = {e['link_target']: e['link_count'] for e in itr}

    ids = [{'id': eid} for eid in entity_to_link_count.keys()]
    cluster_enities = await Cluster.get_multi_async(ids)
    return cluster_enities, entity_to_link_count
