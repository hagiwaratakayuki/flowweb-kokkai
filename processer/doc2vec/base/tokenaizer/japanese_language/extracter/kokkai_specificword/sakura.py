
import re

from doc2vec.tokenaizer.extractor.fix_word import RegexExtractor

extract = RegexExtractor(re.compile(r'桜を.る会'), "桜を見る会")
