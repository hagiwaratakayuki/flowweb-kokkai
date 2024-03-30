def start_end(start: int, end: int):
    return '_'.join([str(token).rjust(4, '0') for token in [start, end]])


def name_escape(name: str):
    return name.encode().hex()


def name_unescape(escaped: str):
    return bytes.fromhex(escaped).decode()


def get_supersets(name: str):
    splited = name.split('会')
    l_sp = len(splited)

    tail = splited[l_sp - 1]
    if l_sp > 2 or (tail != '' and l_sp == 2):
        supersets = []
        if not tail:
            splited = splited[:-1]
        superset = ''
        for token in splited[:-1]:
            superset += token + '会'
            supersets.append(superset)
        return supersets
