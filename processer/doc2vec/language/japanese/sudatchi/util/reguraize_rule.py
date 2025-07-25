from sudachipy.morpheme import Morpheme


def get(token: Morpheme):
    surface = token.surface()
    if surface.isascii():
        return surface
    return token.normalized_form()
