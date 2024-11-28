from db.speech import Speech
from db.node_body import NodeBody

import asyncio
from routing.entity_types.speech import Speech as SpeechEntity
from routing.entity_types.node_body import NodeBody as NodeBodyEntity


class SpeechResponse(SpeechEntity):
    text: str


async def fetch(id) -> SpeechResponse:
    await asyncio.sleep(0)
    ret: SpeechResponse = {}
    body: NodeBodyEntity = {}

    ret, body = await asyncio.gather(Speech.get_async(id), NodeBody.get_async(id))

    ret['body'] = body['body']

    return ret
