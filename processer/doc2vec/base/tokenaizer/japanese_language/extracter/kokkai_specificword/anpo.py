from doc2vec.tokenaizer.extractor.fix_word import RegexExtractor
import regex as re

extract = RegexExtractor(re.compile(r'(日米)?安保(条約)?'), ["日米安保条約"])
