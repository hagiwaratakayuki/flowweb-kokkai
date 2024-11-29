from token import OP
from typing import Optional
from db import meeting
from .model import Model


class Speech(Model):
    title: str
    meeting_id: str
    meeting: str
    speaker: str
    speaker_id: str
    response_to: Optional[str]
    response_from: Optional[str]
    discussion_id: str
    url: str
    order: int
    session: int
    issue: int
    house: str
    sortkey: str

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("text", "url", "order", 'issue')}
        super().__init__(id, entity_options)
