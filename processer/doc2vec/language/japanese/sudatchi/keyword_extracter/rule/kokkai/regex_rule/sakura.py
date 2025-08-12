import re
from processer.doc2vec.language.japanese.sudatchi.keyword_extracter.rule.component.regex import SudatchiRegexRule


rule = SudatchiRegexRule(re.compile('桜を見る会'), output_word='桜を見る会')
