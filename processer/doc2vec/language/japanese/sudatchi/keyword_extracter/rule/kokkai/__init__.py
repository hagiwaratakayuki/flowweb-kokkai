
from processer.doc2vec.language.japanese.sudatchi.keyword_extracter.rule import base
from processer.doc2vec.language.japanese.sudatchi.keyword_extracter.rule.kokkai import lawname, regex_rule


rule = base.rules + regex_rule.rules + [
    lawname.Rule()
]
