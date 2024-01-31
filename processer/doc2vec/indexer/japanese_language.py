from .cls import Indexer
from typing import Dict, Tuple, List, Union
from collections import deque
from .japanese_language.stopwords import remove_stopwords

class JapaneseLanguageIndexer(Indexer):
    def _extract_keywords(self, filtered_map:Dict, vector, specific_keywords:List[Union[Tuple[str], Tuple[str,str]]]):
       
        
    
            


        cand_words = remove_stopwords([super()._extract_keywords(
            filtered_map, vector, specific_keywords)])
        cand_words = remove_stopwords(cand_words)
        cut_keywords = deque()
        for specific_keyword in specific_keywords:
            cut_keywords.extend(specific_keyword)
        ret = deque()
        for word in cand_words:
            

    
        
        return cand_words
