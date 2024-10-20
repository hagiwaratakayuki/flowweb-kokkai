import asyncio

from .get_linked_node import fetch as fetch_sync
from typing import Optional, Union


async def fetch(node_id: Union[str, int], is_keys_only=False, cursor: Optional[str] = None, limit: int = 10):
    await asyncio.sleep(0)
    return fetch_sync(node_id, is_keys_only, cursor, limit)
