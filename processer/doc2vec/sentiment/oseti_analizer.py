import oseti


class NLTKAnalizer:
    def __init__(self) -> None:
        self._analyzer = oseti.Analyzer()

    def exec(self, text: str) -> dict:
        ret = self._analyzer.analyze(text)
        avg = sum(ret) / len(ret)
        return dict(
            negative=1 - avg,
            positive=avg,
            neutral=0.5,
        )
