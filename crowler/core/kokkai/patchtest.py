import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, PropertyMock
from xml.etree.ElementTree import Element
from ..kokkai import MeetingRecord


class DateParseTester(MeetingRecord):
    def __init__(self):
        pass


class MyTestCase(unittest.TestCase):

    def test_basic(self):
        tester = DateParseTester()
        r = tester.getKanjiTime("""次回は、公報をもってお知らせすることとし、本日は、これにて散会いたします。
                            午後四時四十人分散会""")
        print(r)
