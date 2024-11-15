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
    meeting_ids: str

    def __init__(self, id=None, path_args=[], kwargs={}) -> None:
        entity_options = {
            "exclude_from_indexes": ("meeting_ids",)}
        super().__init__(id, entity_options, path_args, kwargs)
