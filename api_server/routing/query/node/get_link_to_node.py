from db.proxy import Node
from ..pattern import get_by_id_async


async def fetch(node):
    params = [{'id': eid} for eid in node.get('link_to', [])]
    if len(params) == 0:
        return []
    return await Node.get_multi_async(params=params)
