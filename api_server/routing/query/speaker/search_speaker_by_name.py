from db.speaker import Speaker
from routing.query.pattern import cursorfetch
import asyncio


async def fetch(speaker_name, cursor=None, limit=10):
    await asyncio.sleep(0)
    query = Speaker.query()
    query.add_filter('name', '>=', speaker_name)
    query.add_filter('name' '<', speaker_name + '{')
    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)
