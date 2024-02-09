from typing import List, Union, Tuple


class EqIn:
    def __init__(self, value) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return object in self.value


class SpecificKeyword:
    is_force: bool
    headword: str
    subwords: List[str]
    _subwords: List[EqIn]
    _tuple: Union[Tuple, None]

    def __init__(self, headword, subwords=[]) -> None:
        self.headword = headword
        self._subwords = [EqIn(subword) for subword in subwords]
        self._tuple = None
        self.subwords = subwords

    def __eq__(self, __value: object) -> bool:
        return __value in self.headword or __value in self._subwords

    def add_subword(self, subword):
        self.subwords.append(subword)
        self._subwords.append(EqIn(subword))

    def to_extender(self):
        return [(self.headword, ), self.to_tuple()]

    def to_tuple(self):
        if self._tuple is None:
            self._tuple = tuple([self.headword] + self._subwords)
        return self._tuple
