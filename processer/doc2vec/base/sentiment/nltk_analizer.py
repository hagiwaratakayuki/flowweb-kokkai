from nltk.sentiment.vader import SentimentIntensityAnalyzer


class SentimentNLTKAnalizer:
    def __init__(self) -> None:
        self._analyzer = SentimentIntensityAnalyzer()

    def exec(self, text: str) -> dict:
        ret = self._analyzer.polarity_scores(text)
        return dict(
            negative=ret['neg'],
            positive=ret['pos'],
            neutral=ret['neu'],
        )
