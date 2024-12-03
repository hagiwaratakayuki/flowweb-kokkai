from .kokkai_specificword import lawname, super_301, sakura, anpo, uncrc_jp, unionchurch, koupro
from .basic import complex_word, sahen


rule_extractor = [
    koupro.extract,
    anpo.extract,
    uncrc_jp.extract,
    unionchurch.extract,
    lawname.extract,
    super_301.extract,
    sakura.extract,
    complex_word.extract,
    sahen.extract,



]
