
from typing import Any, Dict, Optional, List

from google.cloud.datastore.entity import Entity
from .model import Model


from contract_logics.meeting import encode_moderators_contract, decode_moderators_contract


class Meeting(Model):
    session: int
    issue: int
    name: str
    url: str
    pdf: str
    header_text: str
    moderators: List[Dict[str, Any]]
    moderator_ids: List[str]
    keywords: List[str]
    house: str

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("header_text", "pdf", "url", "moderators",)}
        super().__init__(id, entity_options)

    def get_entity(self, id=None, path_args=None, kwargs=None):
        return encode_moderators_contract(super().get_entity(id, path_args, kwargs))

    @classmethod
    def get(cls, id, *path_args, **kwargs):
        return decode_moderators_contract(super().get(id, *path_args, **kwargs))

    @classmethod
    def get_multi(cls, params) -> Optional[List[Entity]]:
        r = super().get_multi(params)
        if r is None:
            return r
        ret = []
        for e in r:
            ret.append(decode_moderators_contract(e))
        return ret
