from typing import Tuple
from spacy.tokens import Token
type CheckResult = Tuple[bool, int]


class CheckProtocol:
    def __call__(self, token: Token) -> CheckResult:
        pass
