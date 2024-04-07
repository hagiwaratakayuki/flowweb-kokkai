from typing import Iterable, Literal, Tuple, Union
from db.speech import Speech
from routing.entity_types.speech import Speech as SpeechEntity
from routing.query.pattern import cursorfetch
import asyncio


async def fetch(speaker_id, cursor=None, limit=10) -> Tuple[Iterable[SpeechEntity], Union[str, Literal[False]]]:
    await asyncio.sleep(0)
    query = Speech.query()
    query.add_filter('speaker_id', '=', speaker_id)
    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)
