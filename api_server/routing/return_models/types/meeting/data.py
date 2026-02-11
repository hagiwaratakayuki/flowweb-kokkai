

from typing import Any
from pydantic import BaseModel
from typing import List

from api_server.routing.return_models.types.meeting.single import MeetingSingle
from ..speech.overview import SpeechOverview


class InitalSpeaker(BaseModel):
    name: Any
    id: Any


class Discussion(BaseModel):
    speaker: InitalSpeaker
    speeches: List[SpeechOverview]


class MeetingData(BaseModel):
    data: MeetingSingle
    discussions: List[Discussion]
