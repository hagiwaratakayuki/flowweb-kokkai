
from doc2vec.language.japanese.sudatchi.util.matcher.pos_system import medium_category
from sudachipy.morpheme import Morpheme


def matcher(token: Morpheme):
    return medium_category.builder.build('読点') or token.surface() == '・'
