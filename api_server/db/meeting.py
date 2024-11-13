
from typing import Optional, Union

from google.cloud.datastore.entity import Entity
from .model import Model
from typing import List, Union
import json
from contract_logics.meeting import encode_moderators_contract, decode_moderators_contract


class Meeting(Model):
    session: int
    issue: int
    name: str
    url: str
    pdf: str
    session: int
    header_text: str
    moderators: str
    moderator_ids: List[str]
    keywords: List[str]
