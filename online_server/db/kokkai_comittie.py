from .model import Model
from google.cloud.datastore.key import Key
from typing import List


class KokkaiComittie(Model):
    name: str
    supersets: list[str]
    start: int
    end: int
    start_end: str


class KokkaiComittieAndSession(Model):
    name: str
    house: str
    session: int
    issue_count: int
