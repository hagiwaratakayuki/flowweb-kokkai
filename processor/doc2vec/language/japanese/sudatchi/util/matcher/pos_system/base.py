

from doc2vec.language.japanese.sudatchi.singleton import SudachiDictionary

none_tuple = (None,)


class SudatchiMatcherGenerater:
    def __init__(self, number):

        self.wildcard_tuple = none_tuple * number

    def build(self, word):
        condition = self.wildcard_tuple + (word, )

        return SudachiDictionary.pos_matcher([condition])
