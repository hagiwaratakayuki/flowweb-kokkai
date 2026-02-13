from typing import Type
from doc2vec.base.facade.tokenaizer_postprocess_doc2vec.builder.root import TokenaizerPostprocessMixinRoot
from .filter import WordbaseSentimentFilter


class WordbaseSentimentFilterMixin(TokenaizerPostprocessMixinRoot):
    filter_class: Type[WordbaseSentimentFilter] = WordbaseSentimentFilter

    def use_wordbase_sentiment(self, posi_words, nega_words, arg_keyword='sentiment_anarizer', **kwargs):
        self.postprocesser_filters.append(
            self.filter_class(
                posi_words=posi_words,
                nega_words=nega_words,
                arg_keyword=arg_keyword,
                **kwargs
            )
        )
        return self
