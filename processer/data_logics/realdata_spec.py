import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, call
from doc2vec.base.doc2vec import Doc2Vec
import numpy as np
from data_loader.dto import DTO
from data_logics import save
from data_loader import nasa_sti


class Mock:
    def __getitem__(self, key):
        return np.random.rand(10)

    def __contains__(self, key):
        return True


class MyTestCase(unittest.TestCase):

    @patch("gensim.models.keyedvectors.KeyedVectors.load_word2vec_format")
    def test_basic(self, lm_model_loader: MagicMock):
        lm_model_loader.return_value = Mock()
        with patch("db.model.client") as client_mock:
            print(save.process(nasa_sti.load))
