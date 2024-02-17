
import MeCab
from collections import deque

import re
from utillib import envinit
from .japanese_language import rule_extractor

KUUHAKU = re.compile('\s+')


tagger = MeCab.Tagger(envinit.read('MeCab').get('config', ''))


class MeCabTokenazier:

    def exec(self, text: str):

        filter = ["", "EOS"]
        results = deque()

        verbs = deque()
        sentences = text.split("。")
        senetence_number = 0
        tokens = deque()
        parse_results = deque()

        for resultline in tagger.parse(text).splitlines():

            if resultline in filter:
                continue

            face, datast = KUUHAKU.split(resultline, 1)
            datas = datast.split(",")
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
        for extractor in rule_extractor:
            specific_words = extractor(specific_words, parse_results)

        return results, specific_words
