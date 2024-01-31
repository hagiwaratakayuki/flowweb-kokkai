from .basic import Remover
from .kanj_ichimoji import kanji_itchimoji
from .o_kanji import o_kanji

preg_remover = Remover(
    [
        kanj_ichimoji,
        o_kanji
    ]
)
