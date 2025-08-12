from email.policy import default
from typing import Optional, Union

from gensim.models import KeyedVectors
from collections import deque
import numpy as np
import os
import logging

from utillib.random_projection import projection
logging.basicConfig(level=logging.INFO)
kv: Union[KeyedVectors, None] = None
projected = {}

MODEL_PATH = 'model/cc.ja.300.vec'
KV: Optional[KeyedVectors] = None


class LoderFunctionClass:
    kv: Union[KeyedVectors, None]
    default_path: str

    def __init__(self, default_path: str):

        self.default_path = default_path

    def load(self, model_path=MODEL_PATH, base_path='') -> KeyedVectors:
        global KV
        if KV is None:
            base_path = base_path or os.getcwd()
            targetpath = os.path.join(base_path, model_path)

            KV = self._load(targetpath)

            logging.info('model load ' + targetpath)

    def _load(self, targetpath):
        pass


class LoadWord2VecFormat(LoderFunctionClass):
    def _load(self, targetpath):
        return KeyedVectors.load_word2vec_format(targetpath)


loadWord2VecFormat = LoadWord2VecFormat(MODEL_PATH)


class LoadKeyedVectors(LoderFunctionClass):
    def _load(self, targetpath):
        return KeyedVectors.load(targetpath)


loadKeyedVectors = LoadKeyedVectors(MODEL_PATH)


class Vectorizer:
    _kv: KeyedVectors

    def __init__(self, model_path=None, basepath='', loader: Optional[LoderFunctionClass] = None) -> None:
        self._model_path = model_path or MODEL_PATH
        self._base_path = basepath
        _loader = loader or loadKeyedVectors
        _loader.load(model_path=self._model_path,
                     base_path=self._base_path)

    def exec(self, word):
        if word in KV:
            return KV[word]
        return False

    def exec_dict(self, words):
        global projected

        ret = {}
        unprojected_vecs = deque()
        unprojected_words = deque()
        unprojected_count = 0
        hit_count = 0
        unhit_count = 0

        for word in words:

            if word in projected is True:

                ret[word] = projected[word]
            elif word not in kv:

                continue
            else:

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

        return ret
