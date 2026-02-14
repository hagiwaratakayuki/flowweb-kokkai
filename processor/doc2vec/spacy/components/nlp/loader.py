import spacy
CACHE = {}


def loadnlp(model_name):
    if model_name in CACHE:
        return CACHE[model_name]

    nlp = spacy.load(model_name)
    CACHE[model_name] = nlp
    return nlp
