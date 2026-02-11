

from typing import Optional
from routing.entity_types.speech import Speech as SpeechEntity
from db.speech import Speech


SpeechMultiResponse = Optional[list[SpeechEntity]]


def fetch(ids) -> SpeechMultiResponse:
    return Speech.get_multi([{'id': id} for id in ids])
