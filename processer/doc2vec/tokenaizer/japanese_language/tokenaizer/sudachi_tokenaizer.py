
from sudachipy import dictionary
from sudachipy import tokenizer


from ...japanese_language import rule_extractor
from .template import TokenazierTemplate
mode = tokenizer.Tokenizer.SplitMode.C


tokenizer_obj = dictionary.Dictionary().create()


class MeCabTokenazier(TokenazierTemplate):

    def _parse(self, text):

        return [(m.surface(), m.part_of_speech(),) for m in tokenizer_obj.tokenize(text, mode)]
