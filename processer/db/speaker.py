from api_server.routing.query import comittie
from .model import Model


class Speaker(Model):
    name: str
    group: str
    position: str
    session: int
    role: str
    house: str
    comittie: str
