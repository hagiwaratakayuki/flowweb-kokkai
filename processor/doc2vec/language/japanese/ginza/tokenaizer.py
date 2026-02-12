
from collections import deque
from typing import Any, Tuple

import spacy
import spacy.tokens

from doc2vec.base.protocol.tokenizer import AbstarctTokenizerClass


nlp = spacy.load('ja_ginza')


class SudatchiTokenizer(AbstarctTokenizerClass):

    def parse(self, arg: Tuple[str, Any]):

        text, data_id = arg

        splited = text.split('。')
        parse_result = deque()
        byte_length = 0

        chunk = ''
        for split in splited:
            if not split:
                continue
            line = split + '。'
            line_len = len(line.encode(errors='replace'))
            next_byte_length = line_len + byte_length

            if next_byte_length > 49149:

                parse_result.append(nlp(chunk))
                chunk = line

                byte_length = line_len
            else:
                chunk += line
                byte_length = next_byte_length

        return spacy.tokens.Doc.from_docs(parse_result), data_id
