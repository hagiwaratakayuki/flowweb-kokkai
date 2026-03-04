

from typing import Any, Tuple

import spacy
import spacy.tokens

from doc2vec.spacy.components.tokenaizer.cls import SpacyToknaizer

import warnings
warnings.filterwarnings('ignore', message=".*Skipping unsupported user data.*")
warnings.simplefilter('ignore')


class GinzaTokenaizer(SpacyToknaizer):

    def parse(self, arg: Tuple[str, Any]):

        text, data_id = arg
        nlp = self._get_language_model()
        splited = text.split('。')
        parse_result = []
        byte_length = 0

        chunk = ''

        for split in splited:
            if not split:
                continue
            line = split + '。'
            line_len = len(line.encode(errors='replace'))
            next_byte_length = line_len + byte_length

            if next_byte_length > 49149:

                parse_result += nlp(chunk).to_array()
                chunk = line

                byte_length = line_len
            else:
                chunk += line
                byte_length = next_byte_length
        if byte_length > 0:
            parse_result.append(nlp(chunk))

        if text:

            return spacy.tokens.Doc.from_docs(parse_result), data_id
        return nlp(''), data_id
