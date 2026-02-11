from typing import Iterable, Literal, Optional, Tuple, Union
from db.speech import Speech
from routing.entity_types.speech import Speech as SpeechEntity
from routing.query.pattern import cursorfetch
from google.cloud.datastore.query import PropertyFilter
import asyncio


async def fetch(speaker_id, cursor=None, limit: Optional[int] = 10) -> Tuple[Iterable[SpeechEntity], Union[str, Literal[False]]]:
    await asyncio.sleep(0)
    query = Speech.query()
    query.add_filter(filter=PropertyFilter('speaker_id', '=', speaker_id))
    if limit is None:
        return query.fetch()
    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)
