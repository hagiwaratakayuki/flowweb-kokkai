
from ast import Tuple
from typing import Any, Callable, Iterable, Optional


class TokenDTO:
    _faces: Optional[Iterable[str]]

    def __init__(self):
        self._faces = None

    def get_norm(self):
        if self._faces == None:
            self._faces = self.get_norm()
        return self._faces

    def get_sents(self) -> Iterable[Iterable[Any]]:
        pass

    def _get_faces(self):
        pass


class TokenizerCls:
    def parse(self, arg: Tuple[str, Any]) -> Tuple[TokenDTO, Any]:
        pass
