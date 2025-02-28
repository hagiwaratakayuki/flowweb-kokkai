
from typing import Any


class FixwordSet:
    def __init__(self, wordset: set) -> None:
        self._wordset = wordset

    def __call__(self, words) -> Any:
        return [word for word in words if word not in self._wordset]
