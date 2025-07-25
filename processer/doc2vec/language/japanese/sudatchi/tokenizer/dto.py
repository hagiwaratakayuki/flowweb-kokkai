from collections import deque
from typing import List
from doc2vec.base.protocol.tokenizer import TokenDTO
from sudachipy.morpheme import Morpheme


class SudatchiDTO(TokenDTO):
    tokens: List[Morpheme]

    def __init__(self, tokens: List[Morpheme]):
        self.tokens = tokens

        super().__init__()

    def _get_faces(self):
        return set([m.normalized_form() for m in self.tokens])

    def _get_sents(self):
        sents = deque()
        sent = deque()
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
