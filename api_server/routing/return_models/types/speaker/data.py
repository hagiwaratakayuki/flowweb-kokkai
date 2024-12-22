from typing import List, Tuple
from pydantic import BaseModel

from routing.return_models.types.speech.overview import SpeechOverview
from .single import SpeakerSingle


class SpeakerData(BaseModel):
    speaker: SpeakerSingle
    same_names: List[Tuple[str, List[SpeakerSingle]]]
    speehes: List[SpeechOverview]
