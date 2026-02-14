from typing import List
from .rule import onn_and_sahen, minasama
from .components import protocol

rules: List[protocol.CheckProtocol] = [onn_and_sahen.rule, minasama.rule]


def check(token: protocol.Token):
    for rule in rules:
        flag, slide = rule(token=token)
        if flag:
            return flag, slide
    return False, 0
