from db.speech import Speech
from routing.query.pattern import cursorfetch
import asyncio


async def fetch(speaker_id, cursor=None, limit=10):
    await asyncio.sleep(0)
    query = Speech.query()
    query.add_filter('speaker_id', '=', speaker_id)
    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)
