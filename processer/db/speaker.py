from click import group
from .model import Model


class Speaker(Model):
    group: str
    name: str
    position: str
    session: int
    role: str
    house: str
