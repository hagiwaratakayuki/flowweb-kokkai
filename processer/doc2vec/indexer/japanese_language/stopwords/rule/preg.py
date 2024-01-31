from typing import Any
import regex

from typing import List


class Rule:
    def __init__(self, pattern: str, flags=regex.U, is_positive_capture=False,  **options) -> None:
        self._pt = regex.compile(pattern=pattern, flags=flags, **options)
        self._is_positive_capture = is_positive_capture

    def __call__(self, words: List[str]) -> List[str]:

        return [word for word in words if self._pt.search(word) is None == self._is_positive_capture]
