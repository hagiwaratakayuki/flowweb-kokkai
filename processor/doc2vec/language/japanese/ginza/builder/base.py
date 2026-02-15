

from regex import R
from doc2vec.language.japanese.ginza.components.sentiment import words
from doc2vec.language.japanese.ginza.components.tokenaizer.cls import GinzaTokenizer
from doc2vec.spacy.components.builder.sequence_doc2vec import SpacySequenceDoc2VecBuilder
from ..components.keyword_extractor.kokkai_rule import base_extract_rules


class SpacyGinzaJapaneseLanguageDoc2VecBuilderBase(SpacySequenceDoc2VecBuilder):
    tokenaier_class = GinzaTokenizer

    def __init__(self, rules=base_extract_rules, stopword_rules=[], keyword_limit=5):
        super().__init__()
        self.set_model_configure('ja_ginza')
        self.use_keyword_extractor(
            rules=rules, stopword_rules=stopword_rules, keyword_limit=keyword_limit)
        self.use_wordbase_sentiment(
            posi_words=words.posiwords, nega_words=words.negwords)
