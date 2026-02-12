from collections import defaultdict, deque
from operator import itemgetter

import re
from typing import Any, Dict, List, Optional, Type

import numpy as np

from doc2vec.base.protocol.sentiment import SentimentResult
from data_loader.dto import DTO
from doc2vec.base.protocol.keyword_extractor import KeywordExtractRule, ExtractResultDTO, AbstractKeywordExtractor, StopwordRule

from doc2vec.base.protocol.postprocessor import DocVectorType, KeywordsType
from doc2vec.base.protocol.vectorizer import WordVectorizer
from doc2vec.base.protocol.tokenizer import TokenDTO

from doc2vec.util.specified_keyword import SpecifiedKeyword


SCORE_KEY = itemgetter(1)


class BasicKeywordExtractor(AbstractKeywordExtractor):
    vectoraizer: WordVectorizer

    def __init__(self, rules: List[KeywordExtractRule], stopword_rules: List[StopwordRule], vectoraizer: WordVectorizer, keyword_limit=5, result_class: Optional[Type[ExtractResultDTO]] = None, ):
        self.rules = rules
        self.keyword_limit = keyword_limit
        self.result_class = result_class or ExtractResultDTO
        self.stopword_rules = stopword_rules
        self.vectoraizer = vectoraizer

    def exec(self, parse_result: TokenDTO, document_vector: DocVectorType, sentiment_results: SentimentResult, dto: DTO, token_2_vector: Dict[Any, np.ndarray], postprocessor: Any, mean_center: np.ndarray) -> KeywordsType:

        results = self.result_class()
        for rule in self.rules:
            results = rule.execute(
                parse_result=parse_result,
                document_vector=document_vector,
                sentiment_results=sentiment_results,
                dto=dto,
                results=results,
                postprocessor=postprocessor

            )
        for rule in self.stopword_rules:
            results = rule.execute(
                parse_result=parse_result,
                document_vector=document_vector,
                sentiment_results=sentiment_results,
                dto=dto,
                results=results,
                postprocessor=postprocessor

            )
        if len(results.keywords) == 0:

            return []

        result_keywords = results.get_keywords()

        keyword_objects = []
        candiate_keywords: List[SpecifiedKeyword] = []
        for result in result_keywords:
            if result.is_force == True:
                keyword_objects.append(result)
                continue
            candiate_keywords.append(result)

        if len(keyword_objects) == 0:
            pass

        word_to_vector, word_to_vector_length = self.vectoraizer.get_vectors(
            parse_result.get_reguraized_forms())

        canditates_length = len(candiate_keywords)
        canditate_index = 0
        candiate_to_reguraizeds = {}
        vector_index = 0
        index_to_reguraized = {}
        vectors = []
        vectors_length = []

        while canditate_index < canditates_length:
            candiate_keyword = candiate_keywords[canditate_index]
            canditate_index += 1

            token_to_reguraied = parse_result.get_token_to_reguraied(
                candiate_keyword.tokens)
            candiate_to_reguraizeds[candiate_keyword] = token_to_reguraied
            for reguraized in token_to_reguraied.values():
                if reguraized not in word_to_vector:
                    continue
                if reguraized not in index_to_reguraized:
                    index_to_reguraized[vector_index] = reguraized
                    vector_index += 1
                    vectors.append(word_to_vector[reguraized])
                    vectors_length.append(word_to_vector_length[reguraized])
        # mean_lengths = np.linalg.norm(
        #    np.subtract(vectors, mean_center), axis=1)

        # scores = np.divide(mean_lengths, vectors_length)
        scores = vectors_length
        score_index = 0
        reguraized_to_score = {}

        for score in scores:
            reguraized = index_to_reguraized[score_index]
            reguraized_to_score[reguraized] = score
            score_index += 1

        canditate_scores = []

        canditate_index = -1
        canditates_length = len(candiate_keywords)
        while canditate_index < canditates_length:
            candiate_keyword = candiate_keywords[canditate_index]
            canditate_index += 1
            score = np.average([reguraized_to_score[reguraized] for reguraized in parse_result.get_token_to_reguraied(
                candiate_keyword.tokens).values() if reguraized in reguraized_to_score])
            canditate_scores.append((candiate_keyword, score, ))
        vectors = deque()

        canditate_scores.sort(key=SCORE_KEY, reverse=True)
        keyword_objects = []
        canditates_length = len(canditate_scores)
        canditate_index = 0
        while canditate_index < canditates_length and canditate_index < 5:
            keyword_objects.append(canditate_scores[canditate_index][0])
            canditate_index += 1

        keywords = []
        added_keyword = set()
        for keyword_object in keyword_objects:
            for keyword_tuple in keyword_object.to_extender():

                keyword = '/'.join(keyword_tuple)
                if keyword in added_keyword:
                    continue
                added_keyword.add(keyword)
                keywords.append(keyword)

        return keywords

    def _get_score_keys(self, sorce_ids):
        pass
