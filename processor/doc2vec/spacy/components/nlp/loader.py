from typing import Tuple

import spacy
from spacy.matcher import Matcher
from spacy.vocab import Vocab

CACHE = {}


def loadnlp(model_name):

    if model_name in CACHE:
        return CACHE[model_name]

    nlp = spacy.load(model_name)
    CACHE[model_name] = nlp
    return nlp


def load_matcher(model_name) -> Tuple[Matcher, Vocab]:
    nlp = loadnlp(model_name)
    return Matcher(nlp.vocab), nlp.vocab
