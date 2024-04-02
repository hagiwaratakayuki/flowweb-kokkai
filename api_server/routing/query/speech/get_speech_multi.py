

from typing import Any, Optional
from routing.entity_types.speech import Speech as SpeechEntity
from db.speech import Speech


SpeechMultiResponse = Optional[list[SpeechEntity]]


def fetch(ids) -> Any:
    return Speech.get_multi([{'id': id} for id in ids])
