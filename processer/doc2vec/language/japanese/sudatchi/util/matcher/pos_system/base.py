

from processer.doc2vec.language.japanese.sudatchi.singleton import SudachiDictionary


class SudatchiMatcherGenerater:
    def __init__(self, number):
        self.number = number

    def build(self, word):
        return SudachiDictionary.pos_matcher((None,) * self.number + (word,))
