
from typing import Any, Iterable, Optional, Set, Tuple
from abc import ABCMeta, abstractmethod


class TokenDTO(metaclass=ABCMeta):
    _reguraized_forms: Optional[Set[str]]

    def __init__(self):
        self._reguraized_forms = None

    @abstractmethod
    def get_tokens(self) -> Any:
        pass

    def get_reguraized_forms(self) -> Set[str]:
        if self._reguraized_forms == None:
            self._reguraized_forms = self._get_reguraized_forms()
        return self._reguraized_forms

    @abstractmethod
    def get_sents(self) -> Iterable[Iterable[Any]]:
        pass

    @abstractmethod
    def _get_reguraized_forms(self) -> Set[str]:
        pass


class TokenizerCls:
    def parse(self, arg: Tuple[str, Any]) -> Tuple[TokenDTO, Any]:
        pass
