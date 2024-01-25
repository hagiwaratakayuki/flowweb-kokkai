
import MeCab
from collections import deque
import os
import re
KUUHAKU = re.compile('\s+')

_stopwords = {}
with open(os.path.join(os.path.dirname(__file__), 'stopwords.txt'), mode='r', encoding='utf-8') as fp:
    for row in fp:
        _stopwords[row.lower().strip()] = True


class MeCabTokenazier:
    def __init__(self) -> None:
        self._tagger = MeCab.Tagger()

    def exec(self, text: str):

        filter = ["", "EOS"]
        results = deque()

        verbs = deque()
        sentences = text.split("。")
        senetence_number = 0

        for resultline in self._tagger.parse(text).splitlines():
            if resultline in filter:
                continue
            face, datast = KUUHAKU.split(resultline, 2)
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

        return results
