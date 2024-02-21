# Template Pattern for Tokenaizer
import MeCab
from collections import deque

import re
from utillib import envinit


tagger = MeCab.Tagger(envinit.read('MeCab').get('config', ''))


class TokenazierTemplate:
    def __init__(self, extractors) -> None:
        self._extractors = extractors

    def exec(self, text: str, data):

        filter = ["", "EOS"]
        results = deque()

        verbs = deque()
        sentences = text.split("。")
        senetence_number = 0
        tokens = deque()
        parse_results = deque()

        for face, datas in self._parse(text):

            tokens.append((face, datas,))

            if datas[0] == "名詞":
                verbs.append(face)
            if face == "。":
                parse_results.append((sentences[senetence_number], tokens,))
                tokens = deque()

                if len(verbs) == 0:
                    senetence_number += 1
                else:

                    results.append((verbs, sentences[senetence_number],))
                    senetence_number += 1
                verbs = deque()
        if senetence_number < len(sentences):
            parse_results.append((sentences[senetence_number], tokens,))
            if len(verbs) != 0:
                results.append((verbs, sentences[senetence_number],))

        specific_words = []
        for extractor in self._extractors:
            specific_words = extractor(specific_words, parse_results, data)

        return results, specific_words

    def _parse(self, text):
        return []
