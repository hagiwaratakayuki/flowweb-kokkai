from abc import ABCMeta, abstractmethod
from typing import Any, Iterable, List, Tuple
from numpy import ndarray
from regex import W
from doc2vec.base.protocol.keyword_extractor import ExtractResultDTO, StopwordRule
from data_loader.dto import DTO
from doc2vec.base.protocol.sentiment import SentimentResult
from doc2vec.util.specified_keyword import SpecifiedKeyword


class WordStopRule(metaclass=ABCMeta):
    @abstractmethod
    def __call__(self, word: str, tokens: List[Any]) -> List[Any]:
        pass


class Rule(StopwordRule, metaclass=ABCMeta):
    rules: List[WordStopRule]

    def __init__(self, rules: List[WordStopRule]) -> None:
        self.rules = rules

    def execute(self, parse_result: any, document_vector: ndarray, sentiment_results: SentimentResult, dto: DTO, results: ExtractResultDTO, postprocessor: Any) -> List[SpecifiedKeyword]:
        stop_token = self._get_stoptoken(results.source_2_keyword.keys())
        parse_result.remove_kewywords(stop_token)
        return parse_result

    def _get_stoptoken(self, tokens: Iterable[Any]):
        word_to_tokens = self._get_word_to_token(tokens)
        stop_tokens = []
        limit = len(word_to_tokens)
        index = 0
        rule_limit = len(self)
        while index < limit:
            word, tokens = word_to_tokens[index]
            rule_index = 0
            index += 1
            while rule_index < rule_limit:
                rule = self.rules[rule_index]
                rule_index += 1
                stop_tokens += rule.execute(word, tokens)
        return stop_tokens

    @abstractmethod
    def _get_word_to_token(self, tokens) -> List[Tuple[str, List[Any]]]:
        ...
