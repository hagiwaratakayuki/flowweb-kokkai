
from ast import Tuple
from typing import Any, Callable, Optional


class TokenDTO:
    _faces: Optional[str]

    def __init__(self):
        self._faces = None

    def get_faces(self):
        if self._faces == None:
            self._faces = self.get_faces()

    def _get_faces(self):
        pass


class TokenizerCls:
    def parse(self, arg: Tuple[str, Any]) -> Tuple[TokenDTO, Any]:
        pass
