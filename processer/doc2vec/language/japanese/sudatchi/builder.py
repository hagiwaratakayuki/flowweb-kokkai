from operator import index
from turtle import st
from doc2vec.base.builder import vectored_sentiment
from doc2vec.language.japanese.builder import default_sentiment
from doc2vec.language.japanese.sudatchi.indexer import SudatchiIndexer
from doc2vec.language.japanese.sudatchi.tokenizer.cls import SudatchiTokenizer
from processer.doc2vec.language.japanese.sudatchi.keyword_extractor import SudatchiKeywordExtarctor

DefaultModelPath = 'model/chive-1.3-mc90.kv'


def build(extract_rules, stopword_rules, model_path=None):

    index_builder = vectored_sentiment.BuilderClass(
        indexer_clsss=SudatchiIndexer, keyword_extracter_class=SudatchiKeywordExtarctor)
    index_builder.build_vectorizer(model_path=model_path or DefaultModelPath)

    index_builder = default_sentiment.build(bulder=index_builder)
    index_builder.build_keyword_extracter(
        rules=extract_rules, stopword_rules=stopword_rules)
    indexer = index_builder.build_indexer()
    tokenaizer = SudatchiTokenizer()
    return indexer, tokenaizer
