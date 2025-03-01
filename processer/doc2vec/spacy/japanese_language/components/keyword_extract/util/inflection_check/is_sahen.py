from spacy.tokens import Token

from .get_inflection import get_inflection


def check(token: Token):
    return "サ変" in get_inflection(token)
