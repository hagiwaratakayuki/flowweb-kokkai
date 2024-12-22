from typing import Iterable
from db.speaker import Speaker
from routing.entity_types.speaker import Speaker as SpeakerEntity
import asyncio
from google.cloud.datastore.query import PropertyFilter


async def fetch(name, cursor=None, limit=10) -> Iterable[SpeakerEntity]:
    await asyncio.sleep(0)
    query = Speaker.query()

    query.add_filter(filter=PropertyFilter('name', '=', name))
    query.order = ["-session"]
    return query.fetch()


def indexer():
    asyncio.run(fetch('index'))
