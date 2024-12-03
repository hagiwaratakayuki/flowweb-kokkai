
import MeCab
from collections import deque

import re
from utillib import envinit
from ..extracter import rule_extractor
from .template import TokenazierTemplate
KUUHAKU = re.compile(r'\s+')


tagger = MeCab.Tagger(envinit.read('MeCab').get('config', ''))


class MeCabTokenazier(TokenazierTemplate):

    def _parse(self, text):
        filter = ["", "EOS"]
        results = deque()

        for resultline in tagger.parse(text).splitlines():

            if resultline in filter:
                continue

            face, data_st = KUUHAKU.split(resultline, 1)
            datas = data_st.split(",")
            results.append((face, datas,))
        return results
