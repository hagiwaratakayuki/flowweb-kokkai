from .basic import Remover
from .kanji_ichimoji import kanji_itchimoji
from .o_kanji import o_kanji

preg_remover = Remover(
    [
        kanji_itchimoji,
        o_kanji
    ]
)
