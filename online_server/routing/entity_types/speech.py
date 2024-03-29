
from typing import TypedDict



class Speech(TypedDict):
    meeting_id: str
    text: str
    speaker: str
    speaker_id: str
    response_to: str
    response_from: str
    discussion_id: str
    url: str
    order: int
    session: int


