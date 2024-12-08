一般とサ変 = set(['一般', 'サ変接続'])
# data はMeCabの品詞情報


def check_ususal_and_sahen(data):
    return data[1] in 一般とサ変
