
from typing import Any, Iterable, Optional, Set, Tuple


class TokenDTO:
    _reguraized_forms: Optional[Set[str]]

    def __init__(self):
        self._reguraized_forms = None

    def get_tokens(self) -> Any:
        raise Exception('get tokens does not implemented')

    def get_reguraized_forms(self) -> Set[str]:
        if self._reguraized_forms == None:
            self._reguraized_forms = self._get_reguraized_forms()
        return self._reguraized_forms

    def get_sents(self) -> Iterable[Iterable[Any]]:
        pass

    def _get_reguraized_forms() -> Set[str]:
        raise Exception('_get_reguraized_forms does not implemented')


class TokenizerCls:
    def parse(self, arg: Tuple[str, Any]) -> Tuple[TokenDTO, Any]:
        pass
