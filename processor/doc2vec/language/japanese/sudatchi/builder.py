
from doc2vec.base.builder import vectored_sentiment
from doc2vec.language.japanese.builder import default_sentiment
from doc2vec.language.japanese.sudatchi.postprocessor import SudatchiPostprocessor
from doc2vec.language.japanese.sudatchi.tokenizer.cls import SudatchiTokenizer
from doc2vec.language.japanese.sudatchi.keyword_extractor import SudatchiKeywordExtarctor

DefaultModelPath = 'model/chive-1.3-mc90.kv'


def build(extract_rules, stopword_rules, model_path=None):

    index_builder = vectored_sentiment.BuilderClass(
        postprocessor_clsss=SudatchiPostprocessor, keyword_extractor_class=SudatchiKeywordExtarctor)
    index_builder.build_vectorizer(model_path=model_path or DefaultModelPath)

    index_builder = default_sentiment.build(bulder=index_builder)
    index_builder.build_keyword_extractor(
        rules=extract_rules, stopword_rules=stopword_rules)
    postprocessor = index_builder.build_postprocessor()
    tokenaizer = SudatchiTokenizer()
    return postprocessor, tokenaizer
