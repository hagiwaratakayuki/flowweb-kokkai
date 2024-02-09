
import MeCab
from collections import deque
import os
import re
from utillib import envinit

KUUHAKU = re.compile('\s+')


tagger = MeCab.Tagger(envinit.read('MeCab').get('config', ''))


class MeCabTokenazier:

    def exec(self, text: str):

        filter = ["", "EOS"]
        results = deque()

        verbs = deque()
        sentences = text.split("。")
        senetence_number = 0
        parses = deque()

        for resultline in tagger.parse(text).splitlines():

            if resultline in filter:
                continue

            face, datast = KUUHAKU.split(resultline, 1)
            datas = datast.split(",")

            if datas[0] == "名詞":
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
