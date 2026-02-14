from spacy.tokens import Token
from .get_tag import get_tag


def check(token: Token):
    return "副詞可能" in get_tag(token)
