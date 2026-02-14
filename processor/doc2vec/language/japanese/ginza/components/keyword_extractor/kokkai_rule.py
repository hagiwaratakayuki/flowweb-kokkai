
from .base_rule import base_extract_rules
from .rule_component.kokkai import comittie, lawname
extract_rules = base_extract_rules + [comittie.Rule(), lawname.Rule()]
