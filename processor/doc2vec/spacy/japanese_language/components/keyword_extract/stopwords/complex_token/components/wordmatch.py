from typing import Tuple
from doc2vec.spacy.util import word_token_match
from .protocol import Token, CheckProtocol


class Check(CheckProtocol):
    word: str
    target_faces: word_token_match.TargetFaces

    def __init__(self, word: str, target_faces: word_token_match.TargetFaces = word_token_match.DEFAULT_TARGET_FACES):
        self.word = word
        self.target_faces = target_faces

    def __call__(self, token: Token) -> Tuple[bool, int]:
        return word_token_match.check_with_slidecount(token=token, word=self.word, target_faces=self.target_faces)
