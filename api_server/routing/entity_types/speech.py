
from .basetype import BaseType


class Speech(BaseType):
    title: str
    meeting_id: str
    meeting: str
    speaker: str
    speaker_id: str
    response_to: str
    response_from: str
    discussion_id: str
    url: str
    order: int
    session: int
    issue: str
    house: str
