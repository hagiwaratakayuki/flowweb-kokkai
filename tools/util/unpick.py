def exec_unpick(target: dict, unpicks=[]):
    for unpick in unpicks:
        del target[unpick]
    return target
