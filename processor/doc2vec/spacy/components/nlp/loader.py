import spacy
from spacy.matcher import Matcher
CACHE = {}


def loadnlp(model_name):
    if model_name in CACHE:
        return CACHE[model_name]

    nlp = spacy.load(model_name)
    CACHE[model_name] = nlp
    return nlp


def get_matcher(model_name):
    return Matcher(loadnlp(model_name).vocab)
