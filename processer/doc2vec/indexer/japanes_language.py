from .cls import Indexer


class JapaneseLanguageIndexer(Indexer):
    def _extract_keywords(self, filtered_map, vector, specific_keywords):

        scored_keywords = remover.remove([super()._extract_keywords(
            filtered_map, vector, specific_keywords)])[0]

        return scored_keywords
