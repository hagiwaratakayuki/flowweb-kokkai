class Rule:
    def __init__(self, stopwords):
        self.stopwords = stopwords

    def __call__(self, word):
        return word in self.stopwords
