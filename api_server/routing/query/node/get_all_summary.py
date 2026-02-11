
import asyncio
from db.proxy import Node
import itertools


async def fetch(limit: int = 200):
    await asyncio.sleep(0)

    q = Node.query()
    q.order = ['-weight']
    return q.fetch(limit=limit)


def indexer():
    asyncio.run(fetch())
