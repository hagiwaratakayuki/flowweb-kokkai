from spacy.tokens import Token


def get_inflection(token: Token):
    return token.morph.get("Inflection")
