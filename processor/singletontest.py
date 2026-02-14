import spacy
cache = {}


def loadnlp(model_name):
    if model_name in cache:
        return cache[model_name]

    nlp = spacy.load(model_name)
    cache[model_name] = nlp
    return nlp
