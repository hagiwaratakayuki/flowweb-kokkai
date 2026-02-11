from typing import Any, FrozenSet, Iterable, Iterator, List, Optional, Type, Union, Tuple, Set, TypeVar, Generic
import numpy as np


class EqIn:
    def __init__(self, value, ) -> None:
        self.value = value

    def __eq__(self, __value: object) -> bool:
        return __value in self.value or self.value in __value


empty_set = set()


TokenType = TypeVar('SourceIDType')


class SpecifiedKeyword(Generic[TokenType]):
    is_force: bool
    headword: str
    subwords: List[str]
    is_fixed_headword: bool
    is_allow_add_multiple_subword: bool
    _subwords: List[EqIn]
    _tuple: Union[Tuple, None]
    _target_words: Union[Set, None]

    tokens: Set[TokenType]

    vectors: Optional[List[np.ndarray]]

    def __init__(self, headword, vectors=[], subwords=[], is_force=False, target_words=None, tokens: Iterable[TokenType] = [], is_fixed_headword=False, is_allow_add_multiple_subword=False) -> None:
        self.is_fixed_headword = is_fixed_headword
        self.headword = headword
        self.tokens = set(tokens)
        self.is_allow_add_multiple_subword = is_allow_add_multiple_subword
        self.vectors = vectors
        self._tuple = None

        self.subwords = subwords[:]
        self.is_force = is_force
        if target_words == None:
            self._target_words = target_words
        else:
            if isinstance(target_words, str):
                target_words = [target_words]
            self._target_words = [EqIn(tw) for tw in target_words]

    @property
    def vector(self) -> np.ndarray:
        return np.average(self.vectors, axis=0)

    def set_headword(self, headword):
        self.headword = headword

    def get_headword_length(self):
        return len(self.headword)

    def clone(self):
        ret = self._clone_class()
        ret.add_subword(self.subwords)
        ret.is_fixed_headword = self.is_fixed_headword
        ret.is_force = self.is_force

        ret._target_words = self._target_words

        ret.tokens = self.tokens.copy()

        return ret

    def _clone_class(self):
        return self.__class__(
            headword=self.headword, vectors=(self.vectors or [])[:])

    def __hash__(self):
        return super().__hash__()

    def __eq__(self, __value: object) -> bool:
        if __value == None:
            return False
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

    def to_paires(self):
        return [self.to_tuple()]

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


class BindSpecifiedKeyword(SpecifiedKeyword):
    def __init__(self, headwords: List[str] = [], vectors=[], haystacks: Optional[Iterator[str]] = None, headword=None, subwords=[], is_force=False, target_words=None, source_ids=[], is_fixed_headword=False, is_allow_add_multiple_subword=False) -> None:
        self._headwords = tuple(headwords)
        self._haystacks = haystacks

        super().__init__(headword, vectors, subwords, is_force, target_words,
                         source_ids, is_fixed_headword, is_allow_add_multiple_subword)

    def _clone_class(self):
        return self.__class__(
            headwords=self._headwords, headword=self.headword)

    def index_of(self, needle):
        if self._haystacks is not None:
            for haystack in self._haystacks:
                position = haystack.find(needle)
                if position != -1:
                    return position
            return -1
        return super().index_of(needle)

    def to_extender(self):

        ret = [(headword, ) for headword in self._headwords]
        if len(self.subwords) != 0:
            subwords = tuple(self._flatten(self.subwords, []))
            ret += [headtuple + subwords for headtuple in ret]
        return ret

    def to_paires(self):
        if len(self.subwords) != 0:
            subwords = tuple(self._flatten(self.subwords, []))
            return [(headword, ) + subwords for headword in self._headwords]
        return [(headword, ) for headword in self._headwords]

    def clone(self):
        ret = super().clone()
        ret._headwords = self._headwords
        return ret


SpecifiedKeywordType = Type[SpecifiedKeyword]
BindSpecifiedKeywordType = Type[BindSpecifiedKeyword]
