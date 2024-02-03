from ..cls import Indexer
from typing import Dict, Tuple, List, Union
from collections import deque
from .stopwords import remove_stopwords
from doc2vec.util.specific_keyword import SpecificKeyword


class JapaneseLanguageIndexer(Indexer):
    def _extract_keywords(self, filtered_map: Dict, vector, specific_keywords: List[SpecificKeyword]):

        cand_words = remove_stopwords(super()._extract_keywords(
            filtered_map, vector, specific_keywords))

        keywords_canditates = deque()

        for specific_keyword in specific_keywords:
            if specific_keyword.is_force == False:
                continue
            keywords_canditates.extend(specific_keyword.to_extender())

        for word in cand_words:
            is_cut = False
            for specific_keyword in specific_keywords:
                if word in specific_keyword:
                    is_cut = True
                    keywords_canditates.extend(specific_keyword.to_extender())
                    break

                if is_cut is True:
                    break
            if is_cut is False:
                keywords_canditates.append((word,))

        appended_keywords = set()
        keywords = []
        for keywords_canditate in keywords_canditates:
            if keywords_canditate not in appended_keywords:
                keywords.append(keywords_canditate)
                appended_keywords.update(keywords_canditate)

        return keywords
