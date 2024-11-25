import unittest
from .mecab_tokenaizer import MeCabTokenazier
from doc2vec.util.specific_keyword import SpecificKeyword
from data_loader.dto import DTO


class TestMecabTokenizer(unittest.TestCase):
    def test_lowname(self):
        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"
        res = toknaizer.exec(
            "今回質問したいのは、金商法でございます。この5章第6項のですね、13条であります、この改正について議論したいと思います。", data)
        specific_keyword: SpecificKeyword = res[1][0]
        print(specific_keyword.headword)
        print(specific_keyword.subwords)

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
