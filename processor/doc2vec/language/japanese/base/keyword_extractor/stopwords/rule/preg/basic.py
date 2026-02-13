from typing import Any
import regex
import re


from typing import List


class Pattern:
    def __init__(self, pattern, is_positive_filter=True):
        self._pt = pattern
        self._is_positive_filter = is_positive_filter

    def __eq__(self, __value: object) -> bool:
        self._pt.search(
            __value) is not None and self._is_positive_filter


class RegexRemover:
    def __init__(self, patterns: List) -> None:
        self._patterns = []
        for pattern in patterns:

            if isinstance(pattern, (regex.Pattern, re.Pattern,)):
                self._patterns.append(Pattern(pattern=pattern))
            elif isinstance(pattern, list):
                self._patterns.append(Pattern(*pattern))
            else:
                self._patterns.append(Pattern(**pattern))

    def __call__(self, words: List[str]) -> List[str]:

        return [word for word in words if word not in self._patterns]
