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

    def test_super301(self):

        toknaizer = MeCabTokenazier()
        data = DTO()
        data.published = "1999-07-01"
        res = toknaizer.exec(
            "我が国とスーパー301条については、関係各所と連携を図り、貿易摩擦の解消", data)
        specific_keyword: SpecificKeyword = res[1][0]

        print(specific_keyword.headword)
        print(specific_keyword.subwords)
        for spk in res[1]:
            print(spk.headword)
            print(spk.subwords)
