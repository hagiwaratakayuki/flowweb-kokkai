

from processor.doc2vec.language.japanese.ginza.components.sentiment import words
from processor.doc2vec.language.japanese.ginza.components.tokenaizer.cls import GinzaTokenizer
from processor.doc2vec.spacy.components.builder.sequence_doc2vec import SpacySequenceDoc2VecBuilder


class Builder(SpacySequenceDoc2VecBuilder):
    tokenaier_class = GinzaTokenizer

    def __init__(self):
        super().__init__()
        self.use_wordbase_sentiment(
            posi_words=words.posiwords, nega_words=words.negwords)

    def build(self, chunksize=1000):
        return super().build(chunksize)
