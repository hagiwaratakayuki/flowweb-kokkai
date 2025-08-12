import re
from processer.doc2vec.language.japanese.sudatchi.keyword_extracter.rule.component.regex import SudatchiRegexRule


rule = SudatchiRegexRule(re.compile(r'子どもの権利条約|子どもの権利に関する条約|児童の権利に関する条約'), output_word=[
                         '子どもの権利条約', '子どもの権利に関する条約', '児童の権利に関する条約'], is_bind_output=True, is_force=True)
