from ..cls import Indexer
from typing import Dict, Tuple, List, Union
from collections import deque, OrderedDict
from .stopwords import remove_stopwords
from doc2vec.util.specific_keyword import SpecificKeyword


class JapaneseLanguageIndexer(Indexer):
    def _extract_keywords(self, filtered_map: Dict, vector, specific_keywords: List[SpecificKeyword]):

        cand_words = remove_stopwords(super()._extract_keywords(
            filtered_map, vector, specific_keywords))

        keywords_dict = OrderedDict()

        for specific_keyword in specific_keywords:
            if specific_keyword.is_force == False:
                continue
            keywords_dict.update(
                {k: True for k in specific_keyword.to_extender()})

        for word in cand_words:

            try:
                specific_keyword = specific_keywords[specific_keywords.index(
                    word)]
                keywords_dict.update(
                    {k: True for k in specific_keyword.to_extender()})

            except:
                keywords_dict[(word,)] = True

        return deque(keywords_dict.keys())
