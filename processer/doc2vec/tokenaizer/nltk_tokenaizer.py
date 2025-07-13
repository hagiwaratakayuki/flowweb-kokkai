
# import nltk
import os
nltk = object()

_stopwords = {}
with open(os.path.join(os.path.dirname(__file__), 'stopwords.txt'), mode='r', encoding='utf-8') as fp:
    for row in fp:
        _stopwords[row.lower().strip()] = True

FILTERS = ['NN', 'NNS', 'NNP', 'NNPS']

FILTERS_MAP = dict(zip(FILTERS, [True] * len(FILTERS)))


class NLTKTokenazer:
    def exec(self, text: str, dto):
        results = []

        for line in text.splitlines():
            tokens = nltk.word_tokenize(line)

            tags = nltk.pos_tag(tokens)
            verbs = [
                face for face, tag in tags if tag in FILTERS_MAP and not tag.lower() in _stopwords]
            if len(verbs) == 0:
                continue
            results.append((verbs, line,))

        return results, []
