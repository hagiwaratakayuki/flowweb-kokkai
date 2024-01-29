import oseti

analyzer = oseti.Analyzer()


class OsetiAnalizer:

    def exec(self, text: str) -> dict:
        ret = analyzer.analyze(text)
        positive = sum(ret) / len(ret)
        negative = 1.0 - positive
        if negative == 0 and positive == 0:
            neutral = 1.0
        else:
            neutral = positive / max(negative, positive)
        return dict(
            negative=negative,
            positive=positive,
            neutral=neutral,
        )
