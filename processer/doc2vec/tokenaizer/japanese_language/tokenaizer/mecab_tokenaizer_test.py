import unittest

from data_loader.util import list_runner
from .mecab_tokenaizer import MeCabTokenazier
from doc2vec.util.specific_keyword import SpecificKeyword
from data_loader.dto import DTO
import unicodedata

from data_loader.kokkai_reguraizer import reguraizers


class TestMecabTokenizer(unittest.TestCase):
    def test_lowname(self):
        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"
        res = toknaizer.exec(
            "今回質問したいのは、金商法でございます。この5章第6項のですね、13条であります、この設置基準について議論したいと思います。", data)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)

    def test_aynu(self):

        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"
        res = toknaizer.exec(
            "アイヌ新法について質問させていただきます。", data)

        specific_keyword: SpecificKeyword = res[1][0]

        print(specific_keyword.headword)
        print(specific_keyword.subwords)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)

    def test_sakura(self):

        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"
        res = toknaizer.exec(
            "桜を見る会について質問させていただきます。", data)

        specific_keyword: SpecificKeyword = res[1][0]

        print(specific_keyword.headword)
        print(specific_keyword.subwords)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)

    def test_worker(self):

        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"
        res = toknaizer.exec(
            "根本の問題であるから、この労働者教育に対して十分な処置をせられたいということを希望しておきます。途中でありますが、あと時間的に......。。", data)

        specific_keyword: SpecificKeyword = res[1][0]

        print(specific_keyword.headword)
        print(specific_keyword.subwords)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)

    def test_airgun(self):

        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"

        text = """
        だいぶ時間がおそくなっていますから、間口を広げないでやりたいのですが、あとでこの機構改革に伴った通産省の行政の基本的な姿勢については幾つかお聞きしたいと思うのです。
　      最初に、通産省の扱うことで具体的な問題で一つお聞きしたいのですが、四十六年の三月の衆議院の地方行政委員会で問題になった問題です。当時、幸世物産という会社が韓国から空気散弾銃を大量に輸入していたということが問題になりまして、鋭和Ｂ３という空気散弾銃ですね。この議会で問題になった当時は、すでに二千五百丁輸入されていまして、さらに一万五千丁輸入の申請が出ていたという問題ですが、この問題では、この委員会の中で、当時の後藤田警察庁長官も、この銃は好ましくない、狩猟用としても、また競技用としても認められないということで、その後輸入が禁止されたという事実があるわけですが、この点については、その後この鋭和Ｂ３という空気散弾銃は輸入されていないということで間違いありませんか。
        """
        text = list_runner.run(reguraizers, text=text, data={})

        res = toknaizer.exec(
            text, data)

        specific_keyword: SpecificKeyword = res[1][0]

        print(specific_keyword.headword)
        print(specific_keyword.subwords)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)

    def test_kenpou(self):

        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"

        text = """
        第一に、これは勞働行政の根本になるものでありますから、憲法の第二十七條の必有勞働權に對する政府の見解をお聽きいたしたいと思うのであります。憲法第二十七條の「すべての國民は、勤勞の權利を有し、義務を負ふ。」という解釋でありますが、この解釋につきましては、私の知る範圍において二様の解釋をとられているようであります。すなわち勞働の機會を享受し得るところの權利、いわゆる働こうと思つても働き口のない者は、當然國家から働き口を世話せられるというこの權利として解釋すべきか、あるいはまた單なる勤勞の自由すなわち一種の自由權の一つとして解釋すべきか。政府はこのいずれの解釋によつて、これから強力なる勞働行政を行わんとするのであるか。まずその點を明らかにしたいと思います。"""
        text = list_runner.run(reguraizers, text=text, data={})

        res = toknaizer.exec(
            text, data)

        specific_keyword: SpecificKeyword = res[1][0]

        print(specific_keyword.headword)
        print(specific_keyword.subwords)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)
