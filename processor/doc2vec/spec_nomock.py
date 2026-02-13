import unittest
from operator import itemgetter
from unittest.mock import patch, MagicMock, call
from doc2vec.base.facade.tokenaizer_postprocess_doc2vec.facade_class import Doc2Vec
import numpy as np
from multiprocessing import Pool
from data_loader.dto import DTO


class MyTestCase(unittest.TestCase):

    def test_basic(self):
        # lm_model_loader.return_value = {'pen':np.array([1,2]), 'paper':np.array([3,4]), 'ink':np.array([5,6])}
        vectaizer = Doc2Vec()

        datas = [DTO(
            title='', body='heare is a pen , paper, and ink', data={})]
        with Pool() as pool:
            computed, data_dict = vectaizer.exec(datas=datas, pool=pool)

            print(list(computed))
            print(data_dict)
