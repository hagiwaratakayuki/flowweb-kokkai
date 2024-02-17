from ..cls import Indexer
from typing import Dict, Tuple, List, Union
from collections import deque, OrderedDict
from .stopwords import remove_stopwords
from doc2vec.util.specific_keyword import SpecificKeyword


class JapaneseLanguageIndexer(Indexer):
    def _extract_keywords(self, filtered_map: Dict, vector, specific_keywords: List[SpecificKeyword]):

        _cand_words = remove_stopwords(list(filtered_map))
        if len(_cand_words) == 0:
            cand_words = []

        else:

            _filtered_map = {k: filtered_map[k] for k in _cand_words}
            cand_words = super()._extract_keywords(_filtered_map, vector, specific_keywords)

        keywords_dict = OrderedDict()

        for specific_keyword in specific_keywords:
            if specific_keyword.is_force is False:
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

        return ['/'.join(kw) for kw in keywords_dict.keys()]
