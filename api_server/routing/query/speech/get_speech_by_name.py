from typing import Iterable, Literal, Union, Tuple


from db.speaker import Speaker
from routing.entity_types.speech import Speech as SpeechEntity
import asyncio
from routing.query.pattern import cursorfetch


async def fetch(name, cursor=None, limit=10) -> Tuple[Iterable[SpeechEntity], Union[str, Literal[False]]]:
    await asyncio.sleep(0)
    query = SpeechEntity.query()
    query.add_filter('name' '=', name)
    return cursorfetch.fetch(cursor=cursor, query=query, limit=limit)
