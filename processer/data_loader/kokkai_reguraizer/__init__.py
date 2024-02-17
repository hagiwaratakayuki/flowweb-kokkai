from data_loader.kokkai_reguraizer import kansuuji_houritu, kyujitai, jikosyoukai, kugirisenn, kaxtuko, unicodedata


reguraizers = [
    jikosyoukai.convert,
    kansuuji_houritu.convert,

    kugirisenn.convert,
    kaxtuko.convert,
    unicodedata.convert,
    kyujitai.convert,


]
