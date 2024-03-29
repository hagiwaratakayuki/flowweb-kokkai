
from typing import TypedDict



class KokkaiComittie(TypedDict):
    name: str


class KokkaiComittieMeetings(TypedDict):
    name: str
    house: str
    session: int


