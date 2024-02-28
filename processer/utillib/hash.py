import math
BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"


def encode(x, y, order=20):
    x_axis = 0
    y_axis = 0

    index_number = 1
    codes = []
    while order >= index_number:
        x_side = int(x > x_axis)
        y_side = int(y > y_axis)
        x_axis += (2 * x_side - 1) / 2 ** index_number
        y_axis += (2 * y_side - 1) / 2 ** index_number

        codes.append(x_side)
        codes.append(y_side)
        index_number += 1
    start = 0
    result = ""
    for end in range(5, len(codes) + 5, 5):
        bits = codes[start:end]
        start = end
        code = sum([bits[i] * 2 ** i for i in range(5)])
        result += BASE32[code]
    return result
