from typing import Iterator, List, Union, Tuple, Set

from httpx import head


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
    is_allow_add_multiple_subword: bool
    _subwords: List[EqIn]
    _tuple: Union[Tuple, None]
    _target_words: Union[Set, None]
    line_numbers: set[int]

    def __init__(self, headword, subwords=[], is_force=False, target_words=None, line_numbers: Iterator = [], is_fixed_headword=False, is_allow_add_multiple_subword=False) -> None:
        self.is_fixed_headword = is_fixed_headword
        self.headword = headword
        self.line_numbers = set(line_numbers)
        self.is_allow_add_multiple_subword = is_allow_add_multiple_subword

        self._tuple = None

        self.subwords = subwords[:]
        self.is_force = is_force
        if target_words == None:
            self._target_words = target_words
        else:
            if isinstance(target_words, str):
                target_words = [target_words]
            self._target_words = [EqIn(tw) for tw in target_words]

    def clone(self):
        ret = self.__class__(
            self.headword)
        ret.add_subword(self.subwords)
        ret.is_fixed_headword = self.is_fixed_headword
        ret.is_force = self.is_force

        ret._target_words = self._target_words

        ret.line_numbers = self.line_numbers.copy()
        return ret

    def __eq__(self, __value: object) -> bool:
        ret = False
        if self._target_words is not None:

            ret |= __value in self._target_words
        ret |= __value in self.headword or self.headword in __value

        return ret

    def add_subword(self, subword):
        if isinstance(subword, str):
            self.subwords.append(subword)
        else:
            self.subwords.extend(subword)

    def to_extender(self):
        ret = [(self.headword, )]
        if len(self.subwords) != 0:
            ret.append(self.to_tuple())
        return ret

    def to_tuple(self):
        if self._tuple is None:
            self._tuple = tuple(
                [self.headword] + self._flatten(self.subwords, []))

        return self._tuple

    def _flatten(self, target, init: list):
        if isinstance(target, str):
            init.append(target)
            return init
        try:
            iter(target)

            for t in target:
                self._flatten(t, init)

        except:
            init.append(target)
        return init

    def index_of(self, needle):
        return self.headword.find(needle)

    def clear_subword(self):
        self.subwords = []


class BindSpecificKeyword(SpecificKeyword):
    def __init__(self, headwords: List[str], headword, subwords=[], is_force=False, target_words=None, line_numbers: Iterator = [], is_fixed_headword=False, is_allow_add_multiple_subword=False) -> None:
        self._headwords = tuple(headwords)

        super().__init__(headword, subwords, is_force, target_words,
                         line_numbers, is_fixed_headword, is_allow_add_multiple_subword)

    def to_extender(self):

        ret = [(headword, ) for headword in self._headwords]
        if len(self.subwords) != 0:
            subwords = self._flatten(self.subwords, [])
            ret += [headtuple + subwords for headtuple in subwords]
        return ret
