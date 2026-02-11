
from doc2vec.base.keyword_extractor.stopwords import check_token_include
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.base.stopwords.include import chapter
from sudachipy.morpheme import Morpheme
surface_stopwords = chapter.words
# surface_rule = check_token_include.Rule(stopwords=surface_stopwords)


def rule(token: Morpheme):
    return False
    """
    if surface_rule(word=token.surface()):
        return True
    return False
    """
