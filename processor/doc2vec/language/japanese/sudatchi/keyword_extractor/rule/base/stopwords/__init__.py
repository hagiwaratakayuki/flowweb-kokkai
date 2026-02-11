from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.base.stopwords import include
from doc2vec.util.listed_function import true_break
from sudachipy.morpheme import Morpheme
stopword_rules = [
    # include.rule
]


def matcher(token: Morpheme):
    return true_break(funcs=stopword_rules, token=token)
