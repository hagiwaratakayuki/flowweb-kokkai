from doc2vec.base.protocol.tokenizer import TokenizerCls, TokenDTO

from sudachipy import tokenizer
from sudachipy import dictionary
TokenizerObject = dictionary.Dictionary().create()
DefaultMode = tokenizer.Tokenizer.SplitMode.C


class SudatchiDTO(TokenDTO):
    def __init__(self):
        super().__init__()


class SudatchiTokenizer(TokenizerCls):
    def __init__(self, mode=DefaultMode):
        self.mode = mode

    def parse(self, text, data_id):
        TokenizerObject.tokenize(text=text, mode=self.mode)
