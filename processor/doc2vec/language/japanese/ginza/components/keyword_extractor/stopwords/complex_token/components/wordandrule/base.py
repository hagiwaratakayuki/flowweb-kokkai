from typing import Tuple
from doc2vec.spacy.util import word_token_match
from ..protocol import Token, CheckProtocol, CheckResult


class BaseCheck(CheckProtocol):

    word: str
    target_faces: word_token_match.TargetFaces
    permission_level: word_token_match.PermissionLevel

    def __init__(self, word: str, target_faces: word_token_match.TargetFaces = word_token_match.DEFAULT_TARGET_FACES, permission_level: word_token_match.PermissionLevel = word_token_match.STRICT):
        self.word = word
        self.target_faces = target_faces
        self.permission_level = permission_level

    def __call__(self, token: Token) -> CheckResult:
        is_match, slide = word_token_match.check_with_slidecount(
            token=token, word=self.word, target_faces=self.target_faces, permission_level=self.permission_level)
        if not is_match:
            return is_match, slide
        else:
            return self._rule(token=token, slide=slide)

    def _rule(self, token: Token, slide: int) -> CheckResult:
        pass
