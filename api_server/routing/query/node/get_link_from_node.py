import asyncio
from db.proxy import Node
from typing import Optional, Union
from ..pattern import cursorfetch, flag_keys_only


async def fetch(node_id: Union[str, int], is_keys_only=False, cursor: Optional[str] = None, limit: int = 10):

    await asyncio.sleep(0)
    query = Node.query()
    query.add_filter('link_to', '=', node_id)
    query.order = ["linked_count"]
    flag_keys_only.check(is_keys_only=is_keys_only, query=query)
    return cursorfetch.fetch(query=query, cursor=cursor, limit=limit)


def indexer():
    fetch(0)
