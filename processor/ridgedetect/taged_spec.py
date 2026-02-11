import unittest, random, string
import numpy as np
from unittest.mock import patch,MagicMock, call
from .taged import Taged


 
tags = [
    ''.join([random.choice(string.ascii_letters + string.digits) for i in range(random.randint(1, 10))])
    for n in range(random.randint(5, 20))
    
]

tags_len = len(tags)
tags_indexs_count = tags_len -1


class MyTestCase(unittest.TestCase):
    def test_basic(self):
        n_samples = 100
        tags_map = {
            i:[
                tags[random.randint(0, tags_indexs_count)] for n in range(random.randint(1, tags_len))
            ]
            for i in range(n_samples)
        }
        #print(tags_map)
        vectors = np.random.rand(n_samples, 10)      
        model = Taged()
        model.fit(tags_map=tags_map, vectors=vectors)
        print(model.clusters)
