from doc2vec.spacy.japanese_language.components.keyword_extract.util.tag_check import is_sahen
from .base import BaseCheck, Token, CheckResult


class Check(BaseCheck):
    def _rule(self, token: Token, slide: int) -> CheckResult:
        doc = token.doc
        index = token.i + slide + 1

        if index >= len(doc) - 1:
            return False, 0
        target = doc[index]
        if is_sahen.check(token=target):
            return True, slide + 1
        return False, slide
