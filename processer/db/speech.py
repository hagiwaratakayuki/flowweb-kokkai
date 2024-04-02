from db import meeting
from .model import Model


class Speech(Model):
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

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("text", "url", "order", "meeting")}
        super().__init__(id, entity_options)
