from typing import Iterator
from db.speech import Speech
from routing.entity_types.speech import Speech as SpeechEntity
import asyncio


async def fech(discussion_id) -> Iterator[SpeechEntity]:
    await asyncio.sleep(0)
    query = Speech.query()
    query.add_filter('discussion_id', '=', discussion_id)
    return query.fetch()
