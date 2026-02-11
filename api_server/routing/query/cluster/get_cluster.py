from db.proxy import Cluster
from ..pattern import get_by_id_async


async def fetch(id):

    return await get_by_id_async.pattern(Cluster, id)
