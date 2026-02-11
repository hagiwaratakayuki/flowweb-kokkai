from multiprocessing import Pool
from sudachipy import tokenizer
from sudachipy import dictionary


def parser(text):
    print([m.surface() for m in tokenizer_obj.tokenize(text, mode)])


tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C
target = ['これはテストです'] * 1000
if __name__ == '__main__':
    with Pool(3) as p:
        p.map(parser, target)
