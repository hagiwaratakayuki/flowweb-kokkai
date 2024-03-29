from .model import Model


class Speech(Model):
    meeting_id: str
    speaker: str
    speaker_id: str
    response_to: str
    response_from: str
    discussion_id: str
    url: str
    order: int
    session: int

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("text", "url", "order")}
        super().__init__(id, entity_options)
