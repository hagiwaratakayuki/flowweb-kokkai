import unittest
from unittest.mock import patch, MagicMock
from .kokkai import execute
import numpy as np
from storage.basic import set_project_id
from doc2vec.spacy.japanese_language.doc2vec.kokkai import updateConfig
import os

# updateConfig({'n_process': 1})


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
    @patch('db.model.client')
    @patch('storage.basic.storage')
    @patch('storage.basic.storage')
    @patch('storage.meeting.download')
    def test_basic(self, meeting_download_mock: MagicMock, storage_mock: MagicMock, db_client_mock: MagicMock, kv_mock: MockKeyedVector):

        with patch('db.kokkai_cluster_link.KokkaiClusterLink') as kokkai_cluster_link_mock:
            sideeffects = []
            """
            with open(os.path.abspath('../testdata/kokkai/1-end.json'), "rb") as fp:
                sideeffects.append([fp.read()])
            """
            chunk = []

            with open(os.path.abspath('../testdata/kokkai/212-end.json'), 'rb') as fp:
                chunk.append(fp.read())

            with open(os.path.abspath('../testdata/kokkai/212-plane.json'), 'rb') as fp:
                chunk.append(fp.read())
            sideeffects.append(chunk)
            # sideeffects.append([])
            meeting_download_mock.side_effect = sideeffects
            execute()
