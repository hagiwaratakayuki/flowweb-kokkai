from typing import Optional, Union

from gensim.models import KeyedVectors
from collections import deque

from doc2vec.base.protocol import vectorizer as vectorizer_protocol

import numpy as np
import os
import logging

from utillib.random_projection import projection
logging.basicConfig(level=logging.INFO)

projected = {}
cached_norms = {}
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


class Vectorizer(vectorizer_protocol.WordVectorizer):

    def __init__(self, model_path=None, basepath='', loader: Optional[LoderFunctionClass] = None) -> None:
        self._model_path = model_path or MODEL_PATH
        self._base_path = basepath
        _loader = loader or loadKeyedVectors
        _loader.load(model_path=self._model_path,
                     base_path=self._base_path)

    def get_vector(self, word):
        if word in KV:
            return KV[word]
        return False

    def get_vectors(self, words):
        global projected

        vectors = {}
        lengths = {}
        unprojected_vecs = deque()
        unprojected_words = deque()
        unprojected_count = 0

        for word in words:

            if word in projected is True:

                vectors[word] = projected[word]
                lengths[word] = cached_norms[word]
            elif word not in KV:

                continue
            else:

                vec = KV[word]
                dt = vec.dtype
                dimn = vec.shape[0]

                unprojected_vecs.append(vec)
                unprojected_words.append(word)
                unprojected_count += 1

        if unprojected_count > 0:

            unprojected_array = np.fromiter(
                unprojected_vecs, dtype=(dt, dimn, ), count=unprojected_count)

            projected_array = projection(unprojected_array)

            length_array = np.sqrt(
                np.einsum("ij,ij->i", projected_array, projected_array))
            for word, projected_vec, norm in zip(unprojected_words, projected_array, length_array):
                projected[word] = projected_vec
                lengths[word] = norm
                cached_norms[word] = norm

                vectors[word] = projected_vec

        return vectors, lengths
