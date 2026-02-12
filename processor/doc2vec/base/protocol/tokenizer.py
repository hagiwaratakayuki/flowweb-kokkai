
from typing import Any, Dict, Iterable, Optional, Set, Tuple
from abc import ABCMeta, abstractmethod


class TokenDTO(metaclass=ABCMeta):
    _reguraized_forms: Optional[Set[str]]
    _token_to_reguraied: Optional[Dict[Any, str]]

    def __init__(self):
        self._reguraized_forms = None
        self._token_to_reguraied = None

    @abstractmethod
    def get_tokens(self) -> Any:
        pass

    def get_reguraized_forms(self) -> Set[str]:
        if self._reguraized_forms == None:
            self._reguraized_forms = set(
                self.get_token_to_reguraied().values())
        return self._reguraized_forms

    @abstractmethod
    def get_sents(self) -> Iterable[Iterable[Any]]:
        pass

    @abstractmethod
    def _get_reguraized_forms(self) -> Set[str]:
        pass

    def get_token_to_reguraied(self, tokens=None) -> Dict[Any, str]:
        if self._token_to_reguraied == None:
            self._token_to_reguraied = {token: self._get_reguraized(
                token) for token in self.get_tokens()}
        if tokens != None:
            return {token: self._token_to_reguraied[token] for token in tokens}
        return self._token_to_reguraied

    @abstractmethod
    def _get_reguraized(self, token):
        pass


class TokenizerCls(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, arg: Tuple[str, Any]) -> Tuple[TokenDTO, Any]:
        pass
