
from collections import deque

from doc2vec.base.protocol.tokenizer import TokenizerCls

from sudachipy import tokenizer, dictionary, Morpheme

from doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from doc2vec.language.japanese.sudatchi.singleton import SudachiDictionary


TokenizerObject = SudachiDictionary.create()
DefaultMode = tokenizer.Tokenizer.SplitMode.C


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
            if not split:
                continue
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
