from .model import Model


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
