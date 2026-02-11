
from .basetype import BaseType
from google.cloud.datastore import Entity


class Speaker(BaseType):
    name: str
    position: str
    session: int
    role: str
    house: str
