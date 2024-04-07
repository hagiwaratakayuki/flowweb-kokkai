from db.speaker import Speaker
from routing.entity_types.speaker import Speaker as SpeakerEntity


async def fetch(id) -> SpeakerEntity:
    return await Speaker.get_async(id)
