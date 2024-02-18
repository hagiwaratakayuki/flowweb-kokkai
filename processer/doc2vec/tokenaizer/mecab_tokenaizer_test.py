import unittest
from .mecab_tokenaizer import MeCabTokenazier
from doc2vec.util.specific_keyword import SpecificKeyword


class TestMecabTokenizer(unittest.TestCase):
    def test_lowname(self):
        toknaizer = MeCabTokenazier()
        res = toknaizer.exec("今回質問したいのは、金商法でございます。この5章第6項のですね、13条であります")
        specific_keyword: SpecificKeyword = res[1][0]
        print(specific_keyword.headword)
        print(specific_keyword.subwords)
