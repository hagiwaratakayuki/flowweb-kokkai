from typing import List, Union, Tuple, Set


class EqIn:
    def __init__(self, value, ) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value or self.value in __value


empty_set = set()


class SpecificKeyword:
    is_force: bool
    headword: str
    subwords: List[str]
    _subwords: List[EqIn]
    _tuple: Union[Tuple, None]
    _index: Union[Set, None]

    def __init__(self, headword, subwords=[], is_force=False, is_one_grame=False, index_word=None, index=None) -> None:

        self.headword = headword

        self._tuple = None
        self._subwords = []
        self.subwords = subwords[:]
        self.is_force = is_force
        if index != None:
            self._index = index
            return
        if is_one_grame == False and index_word is None:
            self._index = None
        elif index_word is not None:
            self._index = set(index_word)
        else:
            self._index = set(headword)

    def clone(self):
        ret = self.__class__(self.headword, index=self._index)
        ret.subwords = self.subwords[:]
        ret._subwords = self._subwords[:]
        return ret

    def __eq__(self, __value: object) -> bool:
        if self._index is not None:

            return (set(__value) & self._index) != empty_set
        return __value in self.headword or self.headword in __value

    def add_subword(self, subword):
        self.subwords.append(subword)
        if self._index is None:
            self._subwords.append(EqIn(subword))

    def to_extender(self):
        return [(self.headword, ), self.to_tuple()]

    def to_tuple(self):
        if self._tuple is None:
            self._tuple = tuple([self.headword] + self.subwords)
        return self._tuple
