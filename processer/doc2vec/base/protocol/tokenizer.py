
from typing import Any, Iterable, Optional, Tuple


class TokenDTO:
    _faces: Optional[Iterable[str]]

    def __init__(self):
        self._faces = None

    def get_norm(self):
        if self._faces == None:
            self._faces = self._get_norm()
        return self._faces

    def get_sents(self) -> Iterable[Iterable[Any]]:
        pass

    def _get_norm(self):
        pass


class TokenizerCls:
    def parse(self, arg: Tuple[str, Any]) -> Tuple[TokenDTO, Any]:
        pass
