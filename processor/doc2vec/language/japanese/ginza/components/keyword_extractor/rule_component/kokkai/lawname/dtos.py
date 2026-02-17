

from operator import attrgetter
from typing import List, Union

from processor.doc2vec.language.japanese.ginza.components.keyword_extractor.rule_component.kokkai.lawname.types import CountChapterType, カタカナ章表現の型


class LawDTO:
    start: int
    is_reverse: bool
    face: str
    name: str
    chapter_canditates: List[Union[CountChapterType, カタカナ章表現の型]]
    len: int
    end: int
    is_guess: bool

    def __init__(self, name, start, face='', is_guess=False, end=None):
        self.name = name
        self.start = start
        self.face = face
        self.is_reverse = False
        self.len = len(self.get_face())
        if end == None:

            self.end = self.start + self.len - 1
        else:
            self.end = end
        self.is_guess = is_guess
        self.chapter_canditates = []

    def get_face(self):
        return self.face or self.name

    def is_chapter_exist(self):
        return len(self.chapter_canditates) > 0

    def get_chapters(self) -> List:
        # TODO 章表現の抽出を実装
        pass


startkey = attrgetter('start')


class LawDTOList:
    index: int
    sequence: List[LawDTO]
    now: LawDTO
    len: int

    def __init__(self) -> None:
        self.index = -1
        self.len = 0
        self.sequence = []

    def sort(self):
        self.sequence.sort(key=startkey)

    def get_first(self):
        return self.sequence[0]

    def append(self, lawdto: LawDTO):
        self.sequence.append(lawdto)
        self.len += 1

    def prepend(self, lawdto: LawDTO):
        self.sequence.insert(0, lawdto)
        self.len += 1

    def step(self):
        self.index += 1
        if self.index < self.len:
            self.now = self.sequence[self.index]
            return True
        return False

    def is_last(self):
        return self.index == self.len - 1

    def get_next(self):

        return self.sequence[self.index + 1]

    def rewind(self):
        self.index = -1
