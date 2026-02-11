from doc2vec.tokenaizer.extractor.fix_word import RegexExtractor

import re

extract = RegexExtractor(re.compile(r'(36|三六)協定'), [
                         "三六協定"])
