
from doc2vec.base.keyword_extracter.stopwords import is_include
from doc2vec.language.japanese.sudatchi.keyword_extracter.rule.base.stopwords.include import chapter
from sudachipy.morpheme import Morpheme
surface_stopwords = chapter.words
surface_rule = is_include.Rule(stopwords=surface_stopwords)


def rule(token: Morpheme):
    if surface_rule(word=token.surface()):
        return True
    return False
