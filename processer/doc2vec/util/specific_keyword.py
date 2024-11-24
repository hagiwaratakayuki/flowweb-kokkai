from typing import Iterator, List, Union, Tuple, Set


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
    is_fixed_headword: bool
    _subwords: List[EqIn]
    _tuple: Union[Tuple, None]
    _index: Union[Set, None]
    line_numbers: set[int]

    def __init__(self, headword, subwords=[], is_force=False, is_one_grame=False, index_word=None, index=None, line_numbers: Iterator = [], is_fixed_headword=False) -> None:
        self.is_fixed_headword
        self.headword = headword
        self.line_numbers = set(line_numbers)

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
        if isinstance(subword, str):
            self.subwords.append(subword)
        else:
            self.subwords.extend(subword)
        if self._index is None:
            self._subwords.append(EqIn(subword))

    def to_extender(self):
        ret = [(self.headword, )]
        if len(self._subwords) == 0:
            ret.append(self.to_tuple())
        return ret

    def to_tuple(self):
        if self._tuple is None:
            self._tuple = tuple(
                [self.headword] + self._flatten(self.subwords, []))

        return self._tuple

    def _flatten(self, target, init: list):
        if isinstance(target, str):
            list.append(init)
            return
        try:
            iter(target)

            for t in target:
                self._flatten(t, init)

        except:
            return

    def index_of(self, needle):
        return self.headword.find(needle)

    def clear_subword(self):
        self.subwords = []
        self._subwords = []
