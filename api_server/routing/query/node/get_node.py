from db.proxy import Node
from ..pattern import get_by_id_async


async def fetch(id):
    return await get_by_id_async.pattern(Node, id)
