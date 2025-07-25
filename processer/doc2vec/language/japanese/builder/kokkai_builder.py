
from doc2vec.base.doc2vec import Doc2Vec
from doc2vec.language.japanese.sudatchi import builder
from doc2vec.language.japanese.sudatchi.keyword_extracter.rule.kokkai import kokkai_extract_rule


def build(build_func=builder.build, doc2vec_class=Doc2Vec):
    indexer, tokenaizer = build_func(kokkai_extract_rule)
    return doc2vec_class(indexer=indexer, tokenaizer=tokenaizer, chunksize=100)
