
from doc2vec.language.japanese.sudatchi.util.matcher.pos_system import medium_category
from sudachipy.morpheme import Morpheme

_matcher = medium_category.builder.build('読点')


def matcher(token: Morpheme):
    return _matcher(token) or token.surface() == '・'
