import unittest
from sentiment.nltk_analizer import SentimentNLTKAnalizer


class MyTestCase(unittest.TestCase):
    def test_basic(self):
        analizer = SentimentNLTKAnalizer()
        print(analizer.exec('this is a pen.'))
