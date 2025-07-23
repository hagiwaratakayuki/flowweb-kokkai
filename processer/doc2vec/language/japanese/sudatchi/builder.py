from processer.doc2vec.base.builder import vectored_sentiment
from processer.doc2vec.language.japanese.builder import default_sentiment
from processer.doc2vec.language.japanese.sudatchi.indexer import SudatchiIndexer
from processer.doc2vec.language.japanese.sudatchi.tokenaizer import SudatchiTokenizer

DefaultFilePath = 'model/chive-1.3-mc90.kv'


def build(extract_rules, file_path=DefaultFilePath):

    index_builder = vectored_sentiment.BuilderClass(SudatchiIndexer)
    index_builder = default_sentiment.build(bulder=index_builder)
    index_builder.buide_vectorizer(filepath=DefaultFilePath)
    index_builder.build_keyword_extracter(rules=extract_rules)
    indexer = index_builder.build_indexer()
    tokenaizer = SudatchiTokenizer()
    return indexer, tokenaizer
