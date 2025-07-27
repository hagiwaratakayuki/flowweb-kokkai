from collections import defaultdict
from operator import itemgetter
from typing import Any, Callable, Dict, List, Optional, Type
from spacy.tokens import Doc, Token
import numpy as np

from doc2vec.base.protocol.sentiment import SentimentResult
from data_loader.dto import DTO
from doc2vec.base.protocol.keyword_extracter import KeywordExtractRule, ExtractResultDTO, KeywordExtracterClass

from doc2vec.base.protocol.indexer import DocVectorType

SCORE_KEY = itemgetter(1)


class BasicKeywordExtratcer(KeywordExtracterClass):
    def __init__(self, rules: List[KeywordExtractRule], keyword_limit=5, result_class: Optional[Type[ExtractResultDTO]] = None):
        self.rules = rules
        self.keyword_limit = keyword_limit
        self.result_class = result_class or ExtractResultDTO

    def exec(self, parse_result: Any, vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, token_2_score: Dict[Any, float], indexer: Any):

        results = self.result_class()
        for rule in self.rules:
            results = rule.execute(
                parse_result=parse_result,
                vector=vector,
                sentiment_results=sentiment_results,
                dto=dto,
                results=results,
                indexer=indexer

            )

        if len(results.keywords) == 0:
            return []
        result_keywords = results.get_keywords()
        keyword_objects = [
            result for result in result_keywords if result.is_force == True]

        keyword_scores = []
        for result_keywords in result_keywords:

            if result_keywords.is_force:
                continue
            score = 0.0
            for source_id in result_keywords.source_ids:
                score += token_2_score[source_id]
            keyword_scores.append((result_keywords, score, ))
        keyword_scores.sort(key=SCORE_KEY, reverse=True)
        count = 0
        for keyword, score in keyword_scores:
            keyword_objects.append(keyword)
            count += 1
            if count >= 5:
                break
        keywords = sum([['/'.join(tuples) for tuples in keyword_object.to_extender()]
                       for keyword_object in keyword_objects], [])
        return keywords
