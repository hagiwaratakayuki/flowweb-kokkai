
import MeCab
from collections import deque

import re
from utillib import envinit
from ...japanese_language import rule_extractor
from .template import TokenazierTemplate
KUUHAKU = re.compile('\s+')


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
            results.appnd((face, datas,))
        return results
