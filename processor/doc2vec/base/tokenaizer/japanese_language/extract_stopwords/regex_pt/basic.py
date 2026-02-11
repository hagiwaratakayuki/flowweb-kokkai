import re


class RegexEq:
    def __init__(self, pattern: re.Pattern) -> None:
        self._pattern = pattern

    def __eq__(self, value: str) -> bool:
        return self._pattern.search(value) != None
