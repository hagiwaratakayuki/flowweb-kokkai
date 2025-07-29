from processer.doc2vec.base.keyword_extracter.rule.regex import RegexRule
from processer.doc2vec.language.japanese.sudatchi.tokenizer.dto import SudatchiDTO
from processer.doc2vec.language.japanese.sudatchi.util.token_search import token_searcher


class SudatchiRegexRule(RegexRule):
    def _search_tokens(self, parse_result, matches):
        return set(token_searcher.search(matches=matches, parse_result=parse_result).keys())
