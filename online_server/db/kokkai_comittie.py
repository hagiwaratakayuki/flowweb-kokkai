from .model import Model
from google.cloud.datastore.key import Key
from typing import List


class KokkaiComittie(Model):
    name: str


class KokkaiComittieMeetings(Model):
    name: str
    house: str
    session: int
