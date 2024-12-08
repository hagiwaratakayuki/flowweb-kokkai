from .kokkai_specificword import lowname, super_301, sakura, anpo, uncrc_jp, unionchurch, koupro, sannroku
from .basic import complex_word, sahen


rule_extractor = [
    sannroku.extract,
    koupro.extract,
    anpo.extract,
    uncrc_jp.extract,
    unionchurch.extract,
    super_301.extract,
    sakura.extract,
    lowname.extract,
    complex_word.extract,
    sahen.extract,



]
