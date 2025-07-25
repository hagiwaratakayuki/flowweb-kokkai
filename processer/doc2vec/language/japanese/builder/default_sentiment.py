from doc2vec.base.builder import vectored_sentiment
posi_words = ['優れる', '良い', '喜ぶ', '褒める', '賢い', '生かす', '祝う', '功績', '賞', '嬉しい', '才知', '徳', '才能', '素晴らしい', '芳しい', '称える',
              '適切', '崇める', '助ける', '忠実', 'にぎやか', '美しい', '雄雄しい', '幸い', '吉兆', '秀でる', '味方']

nega_words = ['醜い', '劣る', '悪い', '悲しむ', '罵る', '卑しい', '下手', '苦しむ', '敵', '厳しい', '難しい', '難い',
              '不適切', '惨い', '責める', '敵', '背く', '嘲る', '苦しめる', '辛い', '寂しい', '罰', '貶める']


def build(bulder: vectored_sentiment.BuilderClass):

    return bulder.build_sentiment_anarizer(posi_words=posi_words, nega_words=nega_words)
