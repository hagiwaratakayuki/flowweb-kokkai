

from typing import Dict
from .basic import BasicJapaneseLanguageDoc2Vec
from ..components.keyword_extract.kokkai import KokkaiKeywordExtractor


CONFIG = {}


class KokkaiJapaneseLanguageDoc2Vec(BasicJapaneseLanguageDoc2Vec):
    def __init__(self, keyword_extractor_class=KokkaiKeywordExtractor, vectoraizer=None, sentiment=None, n_process=None, batch_size=1000, spacy_cofing={}):

        super().__init__(keyword_extractor=keyword_extractor_class(), vectoraizer=vectoraizer,
                         sentiment=sentiment, n_process=n_process, batch_size=batch_size, spacy_cofing=spacy_cofing)


def updateConfig(config: Dict):
    global CONFIG
    CONFIG.update(config)


def builder():
    return KokkaiJapaneseLanguageDoc2Vec(**CONFIG)
