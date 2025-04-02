from typing import Tuple
from doc2vec.spacy.util import word_token_match
from ..protocol import Token, CheckProtocol, CheckResult


class BaseCheck(CheckProtocol):

    word: str
    facetypes: word_token_match.FaceTypes
    permission_level: word_token_match.PEEMISSION_LEVEL

    def __init__(self, word: str, facetypes: word_token_match.FaceTypes = word_token_match.DEFAULT_FACETYPES, permission_level: word_token_match.PEEMISSION_LEVEL = word_token_match.STRICT):
        self.word = word
        self.facetypes = facetypes
        self.permission_level = permission_level

    def __call__(self, token: Token) -> CheckResult:
        is_match, slide = word_token_match.check_with_slidecount(
            token=token, word=self.word, facetypes=self.facetypes, permission_level=self.permission_level)
        if not is_match:
            return is_match, slide
        else:
            return self._rule(token=token, slide=slide)

    def _rule(self, token: Token, slide: int) -> CheckResult:
        pass
