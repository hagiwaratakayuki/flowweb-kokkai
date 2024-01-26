import oseti


class OsetiAnalizer:
    def __init__(self) -> None:
        self._analyzer = oseti.Analyzer()

    def exec(self, text: str) -> dict:
        ret = self._analyzer.analyze(text)
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
