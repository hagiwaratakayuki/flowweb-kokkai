
import MeCab
from collections import deque
import os
import re


KUUHAKU = re.compile('\s+')

_stopwords = {}


tagger = MeCab.Tagger()


class MeCabTokenazier:

    def exec(self, text: str):

        filter = ["", "EOS"]
        results = deque()

        verbs = deque()
        sentences = text.split("。")
        senetence_number = 0

        for resultline in tagger.parse(text).splitlines():
            if resultline in filter:
                continue

            face, datast = KUUHAKU.split(resultline, 1)
            data = datast.split(",")
            if data[0] == "名詞":
                verbs.append(face)
            if face == "。":
                if len(verbs) == 0:
                    senetence_number += 1
                else:

                    results.append((verbs, sentences[senetence_number],))
                    senetence_number += 1
                verbs = deque()

        if len(verbs) != 0:

            results.append((verbs, sentences[senetence_number],))

        return results, []
