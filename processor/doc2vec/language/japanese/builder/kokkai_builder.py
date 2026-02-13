

from doc2vec.base.facade.tokenaizer_postprocess_doc2vec.facade_class import Doc2Vec
from doc2vec.language.japanese.sudatchi import builder
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule import kokkai


def build(build_func=builder.build, doc2vec_class=Doc2Vec):
    postprocessor, tokenaizer = build_func(kokkai.rule, stopword_rules=[])
    return doc2vec_class(postprocessor=postprocessor., tokenaizer=tokenaizer, chunksize=100)
