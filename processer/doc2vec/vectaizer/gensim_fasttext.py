import datetime
from gensim.models import KeyedVectors
import os
import logging
logging.basicConfig(level=logging.INFO)
kv: KeyedVectors | None = None


MODEL_PATH = 'example/fasttext_model/wiki-news-300d-1M.vec'


def loadVectors(filepath=MODEL_PATH, basepath=os.getcwd()) -> KeyedVectors:
    global kv
    if type(kv) == type(None):

        targetpath = os.path.join(basepath, filepath)

        kv = KeyedVectors.load_word2vec_format(targetpath)
        logging.info('model load ' + targetpath)

    return kv  # type: ignore


class Vectaizer:
    _kv: KeyedVectors

    def __init__(self, filepath=MODEL_PATH, basepath=os.getcwd()) -> None:
        self._kv = loadVectors(filepath=filepath, basepath=basepath)

    def exec(self, word):
        if word in self._kv:
            return self._kv[word]
        return False

    def exec_dict(self, words):
        return {k: k in self._kv and self._kv[k] for k in words}
