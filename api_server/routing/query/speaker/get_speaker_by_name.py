from db.speaker import Speaker
from routing.entity_types.speaker import Speaker as SpeakerEntity
import asyncio
from routing.query.pattern import cursorfetch


async def fetch(name, cursor=None, limit=10) -> SpeakerEntity:
    await asyncio.sleep(0)
    query = Speaker.query()
    query.add_filter('name' '=', name)
    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)
