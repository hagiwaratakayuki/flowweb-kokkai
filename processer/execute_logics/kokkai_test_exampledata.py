import unittest
from unittest.mock import patch, MagicMock

from doc2vec.spacy.japanese_language.doc2vec.kokkai import updateConfig
from .kokkai import execute

updateConfig({'n_samples': 1})

import numpy as np
from storage.basic import set_project_id
import os


class MyTestCase(unittest.TestCase):

    @patch('storage.basic.storage')
    @patch('storage.meeting.download')
    def test_basic(self, meeting_download_mock: MagicMock, storage_mock: MagicMock):
        sideeffects = []
        chunk = []
        with open(os.path.abspath('../testdata/kokkai/212-end.json'), 'rb') as fp:
            chunk.append(fp.read())
        with open(os.path.abspath('../testdata/kokkai/212-plane.json'), 'rb') as fp:
            chunk.append(fp.read())
        sideeffects.append(chunk)
        sideeffects.append([])
        meeting_download_mock.side_effect = sideeffects
        execute()
