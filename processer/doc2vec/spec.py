import unittest
from operator import itemgetter
from unittest.mock import patch,MagicMock, call
from doc2vec import Doc2Vec
import numpy as np
from data_loader.dto import BaseDataDTO

class MyTestCase(unittest.TestCase):

    @patch("gensim.models.keyedvectors.KeyedVectors.load_word2vec_format")
    def test_basic(self, lm_model_loader:MagicMock):
        lm_model_loader.return_value = {'pen':np.array([1,2]), 'paper':np.array([3,4]), 'ink':np.array([5,6])}
        vectaizer = Doc2Vec()
        datas = [BaseDataDTO(title='', body='heare is a pen , paper, and ink', data={})]
        print(list(vectaizer.exec(datas=datas)))


       

