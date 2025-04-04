from typing import Tuple
from doc2vec.spacy.util import word_token_match
from .protocol import Token, CheckProtocol


class Check(CheckProtocol):
    word: str
    facetypes: word_token_match.FaceTypes

    def __init__(self, word: str, facetypes: word_token_match.FaceTypes = word_token_match.DEFAULT_FACETYPES):
        self.word = word
        self.facetypes = facetypes

    def __call__(self, token: Token) -> Tuple[bool, int]:
        return word_token_match.check_with_slidecount(token=token, word=self.word, facetypes=self.facetypes)
