from typing import Set
from spacy.tokens import Token


def keywords_match(token: Token, keywords: Set[str], is_nagative_match=False):
    return keywords.isdisjoint((token.norm_, token.lemma_, token.orth_)) == is_nagative_match
