from ast import List
from collections import deque
from functools import cache
from itertools import chain
import re
from typing import Iterable, Optional, Tuple
from doc2vec.base.protocol.tokenizer import TokenizerCls, TokenDTO

from sudachipy import tokenizer, dictionary, Morpheme
TokenizerObject = dictionary.Dictionary().create()
DefaultMode = tokenizer.Tokenizer.SplitMode.C


class SudatchiDTO(TokenDTO):
    tokens: Iterable[Morpheme]
    _tokens_with_positions: Optional[Iterable[Tuple[Morpheme, int, int]]]

    def __init__(self, tokens: Iterable[Morpheme]):
        self.tokens = tokens
        self._tokens_with_positions = None
        super().__init__()

    def _get_faces(self):
        return set([m.normalized_form() for m in self.tokens])

    def _get_sents(self):
        sents = deque()
        sent = deque()
        is_sent_exit = False
        is_multi_sent_exist = False
        for m in self.tokens:
            is_multi_sent_exist = True
            is_sent_exit = True
            sent.append(m)

            if m.normalized_form() == '。':
                sent = deque()
                sents.append(sent)
                is_sent_exit = False
        if is_multi_sent_exist == False:
            return []
        if is_sent_exit == False:
            sents.pop()
        return sents

    def get_tokens_with_position(self):
        if self._tokens_with_positions is None:
            token_with_positins = deque()
            start = 0
            for token in self.tokens:
                len_surface = len(token.surface())
                end = len_surface - 1 + start
                token_with_positins.append((token, start, end, ))
                start += len_surface
        return self._tokens_with_positions


class SudatchiTokenizer(TokenizerCls):
    def __init__(self, mode=DefaultMode):
        self.mode = mode

    def parse(self, text: str, data_id):
        splited = text.split('。')
        parse_result = deque()
        byte_length = 0
        is_chunk_exist = False
        chunk = ''
        for split in splited:
            line = split + '。'
            line_len = len(line.encode(errors='replace'))
            next_byte_length = line_len + byte_length
            is_chunk_exist = True
            if next_byte_length > 49149:

                parse_result.extend(TokenizerObject.tokenize(
                    text=chunk, mode=self.mode))
                chunk = line

                byte_length = line_len
            else:
                chunk += line
                byte_length = next_byte_length
        if is_chunk_exist:
            parse_result.extend(TokenizerObject.tokenize(
                text=chunk, mode=self.mode))

        return SudatchiDTO(parse_result), data_id
