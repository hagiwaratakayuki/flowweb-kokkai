from .node import Node
from typing import Union
from model import Model


class Speech(Model):
    session: int
    meeting_id: str
    text: str
    speaker: str
    speaker_id: str

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("session", "text", )}
        super().__init__(id, entity_options)
