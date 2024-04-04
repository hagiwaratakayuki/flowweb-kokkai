
from .basetype import BaseType



class KokkaiComittie(BaseType):
    name: str
    supersets: list[str]
    start: int
    end: int
    start_end: str


class KokkaiComittieAndSession(BaseType):
    name: str
    house: str
    session: int
    issue_count: int
    meeting_ids: list[str]


