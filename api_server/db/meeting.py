
from typing import Union
from .model import Model
from typing import List
import json


class Meeting(Model):
    session: int
    issue: int
    name: str
    start: str
    end: str
    response_from: str
    url: str
    pdf: str
    session: int
    header_text: str
    moderators: dict
    moderator_ids: List[str]
    keywords: List[str]

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("header_text", "pdf", "url", "moderators")}
        super().__init__(id, entity_options)
