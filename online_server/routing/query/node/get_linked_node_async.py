import asyncio

from .get_linked_node import fetch as fetch_sync
from typing import Optional, Union


async def fetch(node_id: Union[str, int], cursor: Optional[str] = None, limit: int = 10):
    asyncio.sleep(0)
    return fetch_sync(node_id, cursor, limit)
