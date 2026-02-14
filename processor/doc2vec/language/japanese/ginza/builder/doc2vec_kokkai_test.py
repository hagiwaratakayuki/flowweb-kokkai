import unittest

from data_loader.util import list_runner
from .kokkai import KokkaiJapaneseLanguageDoc2Vec
from doc2vec.util.specified_keyword import SpecifiedKeyword
from data_loader.kokkai import DTO


from data_loader.kokkai_reguraizer import reguraizers

doc2vec = KokkaiJapaneseLanguageDoc2Vec(batch_size=1, n_process=1)


class TestDoc2vec(unittest.TestCase):
    def test_lowname(self):

        data = DTO()
        data.published = "1999-07-01"
        text = "今回質問したいのは、金商法でございます。この5章第6条のですね、13項であります、この設置基準について議論したいと思います。"
        data.body = list_runner.run(reguraizers, text=text, data={})
        data.discussion_id = "lowname"
        res = doc2vec.exec([data])
        print(res)

    def test_aynu(self):

        data = DTO()
        data.published = "1999-07-01"
        text = "アイヌ新法について質問させていただきます。"
        data.body = list_runner.run(reguraizers, text=text, data={})
        data.discussion_id = "aynu"
        res = doc2vec.exec([data])
        print(res)

    def test_sakura(self):

        data = DTO()
        data.published = "1999-07-01"
        text = "桜を見る会について質問させていただきます。"
        data.body = list_runner.run(reguraizers, text=text, data={})
        data.discussion_id = "sakura"
        res = doc2vec.exec([data])
        print(res)

    def test_worker(self):

        data = DTO()
        data.published = "1999-07-01"
        text = "根本の問題であるから、この労働者教育に対して十分な処置をせられたいということを希望しておきます。途中でありますが、あと時間的に......。。"
        data.discussion_id = "worker"
        data.body = list_runner.run(reguraizers, text=text, data={})

        res = doc2vec.exec([data])
        print(res)

    def test_airgun(self):

        data = DTO()
        data.published = "1999-07-01"

        text = """だいぶ時間がおそくなっていますから、間口を広げないでやりたいのですが、あとでこの機構改革に伴った通産省の行政の基本的な姿勢については幾つかお聞きしたいと思うのです。
　      最初に、通産省の扱うことで具体的な問題で一つお聞きしたいのですが、四十六年の三月の衆議院の地方行政委員会で問題になった問題です。当時、幸世物産という会社が韓国から空気散弾銃を大量に輸入していたということが問題になりまして、鋭和Ｂ３という空気散弾銃ですね。この議会で問題になった当時は、すでに二千五百丁輸入されていまして、さらに一万五千丁輸入の申請が出ていたという問題ですが、この問題では、この委員会の中で、当時の後藤田警察庁長官も、この銃は好ましくない、狩猟用としても、また競技用としても認められないということで、その後輸入が禁止されたという事実があるわけですが、この点については、その後この鋭和Ｂ３という空気散弾銃は輸入されていないということで間違いありませんか。
        """
        data.discussion_id = "airgun"
        data.body = list_runner.run(reguraizers, text=text, data={})

        res = doc2vec.exec([data])
        print(res)

    def test_kenpou(self):

        data = DTO()
        data.published = "1999-07-01"

        text = """第一に、これは勞働行政の根本になるものでありますから、憲法の第二十七條の必有勞働權に對する政府の見解をお聽きいたしたいと思うのであります。憲法第二十七條の「すべての國民は、勤勞の權利を有し、義務を負ふ。」という解釋でありますが、この解釋につきましては、私の知る範圍において二様の解釋をとられているようであります。すなわち勞働の機會を享受し得るところの權利、いわゆる働こうと思つても働き口のない者は、當然國家から働き口を世話せられるというこの權利として解釋すべきか、あるいはまた單なる勤勞の自由すなわち一種の自由權の一つとして解釋すべきか。政府はこのいずれの解釋によつて、これから強力なる勞働行政を行わんとするのであるか。まずその點を明らかにしたいと思います。"""
        text = list_runner.run(reguraizers, text=text, data={})
        data.discussion_id = "kenpou"
        data.body = text
        res = doc2vec.exec([data])
        print(res)

    def test_unionchurch(self):

        data = DTO()
        data.published = "1999-07-01"
        data.discussion_id = "unionchurch"
        text = """文化庁が遅くとも昭和五十五年と述べている一九八〇年から、統一協会がコンプライアンス宣言なるものを出した二〇〇九年までの二十九年間で二十一件、二〇〇九年にコンプライアンス宣言、すなわち法令遵守を約束してから以降も、現在までの十四年間で十一件にも上るわけですね。つまりは、コンプライアンス宣言以降も問題が継続してきたということであります。継続性ということであります。
　ところが、その統一協会について、文化庁は、二〇一五年に世界基督教統一神霊協会から世界平和統一家庭連合に名称変更を認証したわけです。二〇一五年当時、既に霊感商法で多くの被害者を出し、損害賠償請求を認める判決も出ておりました。世界基督教統一神霊協会として係争中の裁判もあり、社会的にもその名前で認知され、その名前で活動してきた実態があるのに、手前勝手に名称を変えさせるわけにはいかないのは当然であります。
　前川喜平元文部科学事務次官は、一九九七年に僕が文化庁宗務課長だったとき、統一協会が名称変更を求めてきた、実体が変わらないのに名称を変えることはできないと言って断ったと発信をしております。
　改めて聞きますけれども、解散命令請求の根拠として文化庁が悪質性や継続性を認めた民事判決三十二件のうち、既に大半の二十七件もの判決が出ていたにもかかわらず、なぜ二〇一五年八月には名称変更を認めたんですか。次長、お答えいただけますか。
        """

        text = list_runner.run(reguraizers, text=text, data={})
        data.body = text
        res = doc2vec.exec([data])
        print(res)

    def test_complexword_with_count(self):

        data = DTO()
        data.published = "1999-07-01"
        data.discussion_id = "comp_with_c"
        text = """ 散弾空気銃二千丁輸入の件について
        """
        text = list_runner.run(reguraizers, text=text, data={})
        data.body = text
        res = doc2vec.exec([data])
        print(res)
