from collections import deque
from typing import List
from doc2vec.base.protocol.tokenizer import TokenDTO
from sudachipy.morpheme import Morpheme

from doc2vec.language.japanese.sudatchi.util import reguraize_rule


class SudatchiDTO(TokenDTO):
    tokens: List[Morpheme]

    def __init__(self, tokens: List[Morpheme]):

        self.tokens = tokens

        self._tokens_len = None

        super().__init__()

    def get_tokens(self):
        return self.tokens

    def _get_faces(self):
        return set([m.normalized_form() for m in self.tokens])

    def _get_reguraized_forms(self):
        return {reguraize_rule.apply(m) for m in self.tokens}

    def _get_reguraized(self, token):
        return reguraize_rule.apply(token)

    def get_sents(self):
        sents = deque()
        sent = deque()
        sents.append(sent)
        is_last_sent_exit = False
        is_multi_sent_exist = False
        for m in self.tokens:

            is_multi_sent_exist = True
            is_last_sent_exit = True
            sent.append(m)

            if m.normalized_form() == '。':
                sent = deque()
                sents.append(sent)
                is_last_sent_exit = False
        if is_multi_sent_exist == False:
            return []
        if is_last_sent_exit == False:
            sents.pop()
        return sents

    def get_tokens_len(self):
        if self._tokens_len is None:
            self._tokens_len = len(self.tokens)
        return self._tokens_len
