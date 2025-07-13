

from typing import Dict
from .basic import BasicJapaneseLanguageDoc2Vec
from ..components.keyword_extract.kokkai import KokkaiKeywordExtracter


CONFIG = {}


class KokkaiJapaneseLanguageDoc2Vec(BasicJapaneseLanguageDoc2Vec):
    def __init__(self, keyword_extracter_class=KokkaiKeywordExtracter, vectoraizer=None, sentiment=None, n_processes=None, batch_size=10, spacy_cofing={}):

        super().__init__(keyword_extracter_class(), vectoraizer,
                         sentiment, n_processes, batch_size, spacy_cofing)


def updateConfig(config: Dict):
    global CONFIG
    CONFIG.update(config)


def builder():
    return KokkaiJapaneseLanguageDoc2Vec(**CONFIG)
