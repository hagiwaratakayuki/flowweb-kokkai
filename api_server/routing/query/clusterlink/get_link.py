import asyncio
from ....db.cluster_link import ClusterLink


async def fetch(cluster_id):
    await asyncio.sleep(0)
    return ClusterLink.query()
