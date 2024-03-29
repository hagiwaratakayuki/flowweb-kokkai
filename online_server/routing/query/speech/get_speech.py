from db.speech import Speech
import asyncio
from routing.entity_types.speech import Speech


class SpeechResponse(Speech):
    text: str


async def fetch(id):
    ret: SpeechResponse = {
        '': ''
    }
    await asyncio.gather(*[self._put_multi(weight) for weight in weightings])
