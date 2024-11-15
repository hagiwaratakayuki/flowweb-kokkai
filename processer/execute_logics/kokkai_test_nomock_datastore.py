import unittest
from unittest.mock import patch, MagicMock
from .kokkai import execute
import numpy as np
from storage.basic import set_project_id
import os


class MockKeyedVector:
    def __init__(self) -> None:
        self._items = {}

    def __getitem__(self, key):
        if key in self._items:
            return self._items[key]
        else:
            self._items[key] = ((np.random.random(300) - 0.5) * 2) / 100
            return self._items[key]

    def __contains__(self, item):
        return True


class MyTestCase(unittest.TestCase):

    @patch('doc2vec.vectaizer.gensim_fasttext.kv', MockKeyedVector())
    @patch('storage.basic.storage')
    @patch('storage.meeting.download')
    def test_basic(self, meeting_download_mock: MagicMock, storage_mock: MagicMock, kv_mock=MockKeyedVector):
        sideeffects = []
        with open(os.path.abspath('../testdata/kokkai/1-end.json'), "rb") as fp:
            sideeffects.append([fp.read()])
        sideeffects.append([])
        meeting_download_mock.side_effect = sideeffects
        execute()
