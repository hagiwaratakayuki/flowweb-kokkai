from typing import Any
from pydantic import BaseModel


class SpeechOverview(BaseModel):
    id: Any
    meeting_id: str
    meeting: str
    speaker: str
    speaker_id: str
