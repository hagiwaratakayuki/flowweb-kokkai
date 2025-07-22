from collections import defaultdict
from operator import itemgetter
from typing import Callable, Dict, List
from spacy.tokens import Doc, Token
import numpy as np

from doc2vec.base.protocol.sentiment import SentimentResult
from data_loader.dto import DTO
from doc2vec.spacy.components.keyword_extracter.protocol import KeywordExtractRule, ExtractResultDTO
from doc2vec.util.specified_keyword import SpecifiedKeyword

SCORE_KEY = itemgetter(1)


class BasicKeywordExtratcer:
    def __init__(self, rules: List[KeywordExtractRule], keyword_limit=5):
        self.rules = rules
        self.keyword_limit = keyword_limit

    def exec(self, doc: Doc, vector: np.ndarray, sentiment_results: SentimentResult, dto: DTO, token_2_score: Dict[Token, float]):

        results = ExtractResultDTO()
        for rule in self.rules:
            results = rule.execute(
                doc=doc,
                vector=vector,
                sentiment_results=sentiment_results,
                dto=dto,
                results=results,

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
