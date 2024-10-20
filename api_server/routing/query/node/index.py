import asyncio
from routing.query.node import get_linked_node_async


async def node():
    await get_linked_node_async.fetch(node_id='test')
