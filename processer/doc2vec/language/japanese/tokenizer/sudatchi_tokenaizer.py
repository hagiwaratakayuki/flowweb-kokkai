from itertools import chain
from doc2vec.base.protocol.tokenizer import TokenizerCls, TokenDTO

from sudachipy import tokenizer, dictionary, MorphemeList
TokenizerObject = dictionary.Dictionary().create()
DefaultMode = tokenizer.Tokenizer.SplitMode.C


class SudatchiDTO(TokenDTO):
    tokens: MorphemeList

    def __init__(self, tokens: MorphemeList):
        self.tokens = tokens
        super().__init__()

    def _get_faces(self):
        return set(chain.from_iterable([(m.dictionary_form(), m.normalized_form(), m.surface(), ) for m in self.tokens])])


            class SudatchiTokenizer(TokenizerCls):
            def __init__(self, mode=DefaultMode):
            self.mode = mode

            def parse(self, text, data_id):
            return SudatchiDTO(TokenizerObject.tokenize(text=text, mode=self.mode))
