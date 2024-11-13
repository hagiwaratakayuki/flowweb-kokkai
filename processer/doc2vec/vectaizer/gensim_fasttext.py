from typing import Union

from gensim.models import KeyedVectors
from collections import deque
import numpy as np
import os
import logging

from utillib.random_projection import projection
logging.basicConfig(level=logging.INFO)
kv: Union[KeyedVectors,  None] = None
projected = {}

MODEL_PATH = 'model/cc.ja.300.vec'


def loadVectors(filepath=MODEL_PATH, basepath=os.getcwd()) -> KeyedVectors:
    global kv
    if kv is None:

        targetpath = os.path.join(basepath, filepath)

        kv = KeyedVectors.load_word2vec_format(targetpath)
        logging.info('model load ' + targetpath)

    return kv


class Vectaizer:
    _kv: KeyedVectors

    def __init__(self, filepath=MODEL_PATH, basepath=os.getcwd()) -> None:
        self._filepath = filepath
        self._basepath = basepath

    def exec(self, word):
        if word in self._kv:
            return self._kv[word]
        return False

    def exec_dict(self, words):
        global projected
        kv = loadVectors(filepath=self._filepath, basepath=self._basepath)

        ret = {}
        unprojected_vecs = deque()
        unprojected_words = deque()
        unprojected_count = 0
        hit_count = 0
        unhit_count = 0

        for word in words:

            if word in projected is True:
                hit_count += 1
                ret[word] = projected[word]
            elif word not in kv:
                unhit_count += 1
                continue
            else:
                hit_count += 1
                vec = kv[word]
                dt = vec.dtype
                dimn = vec.shape[0]

                unprojected_vecs.append(vec)
                unprojected_words.append(word)
                unprojected_count += 1
        if unprojected_count > 0:

            unprojected_mat = np.fromiter(
                unprojected_vecs, dtype=(dt, dimn, ), count=unprojected_count)
            projected_mat = projection(unprojected_mat)
            for word, projected_vec in zip(unprojected_words, projected_mat):
                projected[word] = projected_vec
                ret[word] = projected_vec
        print('hit:', hit_count)
        print('misshit', unhit_count)
        return ret
