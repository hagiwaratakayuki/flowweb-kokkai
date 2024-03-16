
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
    moderators: List[str]
    moderator_ids: List[str]

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("header_text", "pdf", "url", "moderators")}
        super().__init__(id, entity_options)

    def _get_attr(self, key):
        if key == "moderators":
            return json.dumps(self.moderators)
        return super()._get_attr(key)

    def _set_attr(self, k, v):
        if k == "moderators":
            v = json.loads(v)

        return super()._set_attr(k, v)
