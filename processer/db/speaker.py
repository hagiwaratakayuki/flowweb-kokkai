from model import Model


class Speaker(Model):
    name: str
    position: str
    session: int
    role: str
    house: str

    def __init__(self, id=None) -> None:
        entity_options = {
            "exclude_from_indexes": ("session", "text", )}
        super().__init__(id, entity_options)
