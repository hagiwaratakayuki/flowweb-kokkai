from .model import Model


class Speaker(Model):
    name: str
    position: str
    session: int
    role: str
    house: str
