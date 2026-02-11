from db.speech import Speech
from routing.entity_types.speech import Speech as SpeechEntity
import asyncio
from operator import itemgetter
order_by = itemgetter('order')


async def fech(discussion_id) -> list[SpeechEntity]:
    await asyncio.sleep(0)
    query = Speech.query()
    query.add_filter('discussion_id', '=', discussion_id)
    response: list[SpeechEntity] = list(query.fetch())
    return sorted(response, key=order_by)
