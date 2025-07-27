from sudachipy.morpheme import Morpheme


def apply(token: Morpheme):
    surface = token.surface()
    if surface.isascii():
        return surface
    return token.normalized_form()
