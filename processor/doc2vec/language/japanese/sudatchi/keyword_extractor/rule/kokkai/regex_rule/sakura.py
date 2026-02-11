import re
from doc2vec.language.japanese.sudatchi.keyword_extractor.rule.component.regex import SudatchiRegexRule


rule = SudatchiRegexRule(re.compile('桜を見る会'), output_word='桜を見る会')
