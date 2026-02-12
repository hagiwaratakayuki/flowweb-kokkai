from typing import Type
from doc2vec.base.builder.doc2vec.tokenaizer_postprocessor.root import TokenaizerPostprocessMixinRoot
from doc2vec.base.builder.components.wordbase_sentiment.filter import WordbaseSentimentFilter


class WordbaseSentimentMixin(TokenaizerPostprocessMixinRoot):
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
