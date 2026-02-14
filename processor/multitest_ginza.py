import base64
from multiprocessing import Pool
from tkinter import N
import spacy
import ginza
from data_loader.kokkai_reguraizer.kyujitai import convert
from singletontest import loadnlp
import time

# from doc2vec.spacy.components.commons.const import MAIN_POS
# from doc2vec.tokenaizer.japanese_language.extracter.basic import sahen


# nlp = spacy.load('ja_ginza')
# ginza.set_split_mode(nlp=nlp, mode="A")

text = """
わが國においても、當然これはもつと早く設置されておらなければならなかつたのでございまするが、今日に至つたのでございまして、吉田内閣當時においても設置の考えはあつたのでございまするが、ついにその實現を見ずして、この片山内閣において初めてここにいよいよ設置することにきまりまして、この法案の提出をみるに至つたのでございます。
　この法案を皆さんに御審議を願ふ前に、内閣といたしましては、勞働省設置準備委員會というものを設けまして、關係官廳の官吏竝びに事業者側、勞働者側、その他の民間側の代表者から構成される委員によつて、愼重に勞働省の機構及びその目的等について審議をしたのでございます。この準備委員會の審議の結果を参考として、ここに提出したのが本法案でございます。
　勞働省設置の目的はこの法案第一條に明記いたしてある通り、勞働者の福祉と職業の確保とをはかつて、もつて經濟の與隆と國民生活の安定に寄與したいというのでございます。今日の日本の經濟状態は、私がくどくどここで皆さんに申し上げるまでもなく、資金の面において拘束著しいものがあり、また資材の面においてもようやく底をつくという状態でございまして、今日の日本の經濟の復興、生産の増強ということは、一にかかつて勞働の面からみた生産性の高揚ということが十分に達成されて、勤勞階級のもつておる勞働能率が百パーセントに發揮されなければ、とうてい今日の經濟界の危機は救われないということは、私が申し上げるまでもないと思うのでございます。しかしながらこういうぐあいに生産性の高揚と、勞働能力の發揮をわれわれが期待するためには、ここに強力なる勞働政策を實施しなければならないのでありまして、それがためには、勞働者の福祉と、職業の確保とをはかつて、勞働問題を圓滑に解決處理し、勞働者の生活を確保していくことが必要となつてくるのでございます。
わが國の今日の勞働政策として、あるいは勞働界の現状をみますると、御承知の通り、勞働組合法、勞働關係調整法、勞働基準法等、各種の立法がすでに行われまして、勞働組合運動の方もこれに對應して活發に發展はいたしておりまするが、經濟復興に關する積極的かつ自主的な勞働者の協力を促進すべきである。また勞働關係の健全な調整をしなければならぬ。あるいは勞働者の生活權の保障をもつと強化しなければならぬ。あるいは勞働者の失業對策等もしなければならぬというふうで、問題は山積しておる状態にあるのでございます。政府は、この際こういう現状に即しまして、獨立した勞働省と稱する省をつくることによつて、これらの重要かつ困難なる諸問題を、積極的に取上げてこれを解決していきたいと考えておるのでございます。
　こういう意味におきまして、勞働省をつくることにしたのでございまするが、しからば勞働大臣の所管する事務の範囲はどういうものであるかというと、お手もとに差上げた法案の第二條に書いてある通りでございまして、すなわち勞働組合、勞働關係の調整、勞働に關する啓蒙宣傳、勞働條件、あるいは勞働者災害補償、勞働者災害補償保險及び勞働者の「補護に關する事務、職業の」紹介、指導、補導、その他勞働需給の調整に關する事務、失業對策に關する事務、失業保險に關する事務、勞働統計調査に關する事務、その他、勞働に關する事務を一元的に所掌してまいるのであります。
　この際御参考に申し上げたいことは、船員勞働につきましては、あるいは理論的に言いますと、勞働者へこれを入れて、總括的にやつていくべきではないかという意見もあつたのでございますが、船員勞働の特種性に鑑みまして、また船員勞働は現在運輸省の海運總局でやつてきておる歴史的な事情等を考えまして、これを運輸省に設置することといたしました。但し一般勞働行政と船員勞働との調整統一連絡をはかる必要があるために、勞働省に船員勞働連絡會議——これは假稱でございますが、そういうものを置くことといたしたのでございます。
　勞働省に設置される部局につきましては、第三條、第四條にきめておりますが、大臣官房のほか、勞政局、勞働基準局、婦人少年局、職業安定局、勞働統計調査局の五局を設けたいと思つております。勞政局は、勞働組合法及び勞働關係調整法の施行に關する事務のほかに、勞働運動の健全なる發展のため勞働教育に關する事務等を掌るものでございます。勞働基準局におきましては、勞働基準法の施行事務のほかに、勞働者の災害補償保險、勞働者の福利厚生その他勞働條件及び勞働者の保護に關する事務を掌ることにいたしておるのでございます。婦人少年局、これは新たにできる局でございますが、この局の任務は婦人及び年少勞働者の特殊な勞働問題を所管するのほか、勞働者の家族問題に關する事項竝びに婦人の地位の向上、その他婦人問題の調査及び連絡調整に關する事務を所管することにいたしたいと思います。ただし勞働者の家族問題及び一般婦人問題については、他の各省において、たとえば厚生省、内務省、文部省、そういつた省がそれぞれその主管に屬しておる事務を現在行つておるのでありますが、これらの省に屬しない一般婦人問題もありますので、この勞働省の婦人少年局が中心になつて、これらの省との間の連絡をはかり、かつこれらの省で現在やつておらない問題については、これを勞働省の婦人少年局で處理していきたいと考えております。職業安定局につきましては、勞務の需給の調整、失業對策、失業保健、失業手當、その他職業安定に關する事務を所管することになつております。最後に勞働行政の合理的、科學的運營をはかるために、勞働統計調査局を設けまして、勞働統計調査に關する事務を一元的に所管せしめたいと思つております。これらの五局のほかに、さらに將來情勢の變化に伴つて部局の所掌事務の一部を變更し、または新しい部局を増置する必要が起ることが考えられますので、第三條の第二項において、その點を規定してあるのでございます。その場合においては、政令の定むるところによつて新部局を設けて、省内において部局の所掌事務の一部を變更することができるようにしたいと思つております。なお今まで申し上げた官房、五局のほかに、研究機關といたしまして、從來厚生省に所屬しておりましたところの産業安全研究所を勞働省に移官して、災害豫防に關する調査の研究、竝びにそれに關連のある技術者の養成訓練を行わしめたいと思つております。以上のほか勞働省の部局機關及び職員について必要なる事項は、政令でこれを定めることにいたしたいと思います。
　最後に本法律案の制定に伴いまして、當然起つてくる厚生省の官制竝びに勞働基準法の一部を改正する必要がありまするので、これを附則において改正する規定を設けたのであります。
　以上勞働省設立法案の大要を御説明申し上げたのでございますが、現下の勞働問題の重要性に鑑みまして、何とぞ慎重に御審議くださることは當然でございまするが、こういう事情のもとにございまするから、一日も早く審議を終えさせられんことを特にお願い申し上げる次第であります。はなはだ簡單でございますが、提案の理由を御説明申し上げました。

"""


def example(nlp):

    texts = []
    # print(nlp.batch_size)
    # doc = nlp(convert("アリスは説明します。今日は昨日と決定的に違って駄菓子屋ではなくラーメン屋とスーパーに行きます、と", None))

    # start = time.perf_counter()

    # text = """金商法改正の議論の前進に向けて、議論したいと思います"""
    # text = "夜も遅いので手短に。教育基本法11条の設置基準について"
    # ginza.set_split_mode(nlp=nlp, mode="A")
    # text = "令和4年4月1日に起きた事件について質問します"

    # text = "勞働省設置の目的はこの法案第一條に明記いたしてある通り、勞働者の福祉と職業の確保とをはかつて"
    text = """だいぶ時間がおそくなっていますから、間口を広げないでやりたいのですが、あとでこの機構改革に伴った通産省の行政の基本的な姿勢については幾つかお聞きしたいと思うのです。
　      最初に、通産省の扱うことで具体的な問題で一つお聞きしたいのですが、四十六年の三月の衆議院の地方行政委員会で問題になった問題です。当時、幸世物産という会社が韓国から空気散弾銃を大量に輸入していたということが問題になりまして、鋭和Ｂ３という空気散弾銃ですね。この議会で問題になった当時は、すでに二千五百丁輸入されていまして、さらに一万五千丁輸入の申請が出ていたという問題ですが、この問題では、この委員会の中で、当時の後藤田警察庁長官も、この銃は好ましくない、狩猟用としても、また競技用としても認められないということで、その後輸入が禁止されたという事実があるわけですが、この点については、その後この鋭和Ｂ３という空気散弾銃は輸入されていないということで間違いありませんか。
        """

    # texts.append((convert(text, None), {1: 2}))
    # text = "空気散弾銃千丁を輸入する、そういう表現がところどころに見受けられます"
    # text = "皆様ご指導ご鞭撻のほどよろしくお願いします"
    # text = "白米千枚田は石川県輪島市白米町にある棚田です"
    # text = "イギリス及びスコットランドにおいて、ウィスキーと紅茶の生産量に着目します"
    # text = '憲法第条'

    text = """文化庁が遅くとも昭和五十五年と述べている一九八〇年から、統一協会がコンプライアンス宣言なるものを出した二〇〇九年までの二十九年間で二十一件、二〇〇九年にコンプライアンス宣言、すなわち法令遵守を約束してから以降も、現在までの十四年間で十一件にも上るわけですね。つまりは、コンプライアンス宣言以降も問題が継続してきたということであります。継続性ということであります。
　ところが、その統一協会について、文化庁は、二〇一五年に世界基督教統一神霊協会から世界平和統一家庭連合に名称変更を認証したわけです。二〇一五年当時、既に霊感商法で多くの被害者を出し、損害賠償請求を認める判決も出ておりました。世界基督教統一神霊協会として係争中の裁判もあり、社会的にもその名前で認知され、その名前で活動してきた実態があるのに、手前勝手に名称を変えさせるわけにはいかないのは当然であります。
　前川喜平元文部科学事務次官は、一九九七年に僕が文化庁宗務課長だったとき、統一協会が名称変更を求めてきた、実体が変わらないのに名称を変えることはできないと言って断ったと発信をしております。
　改めて聞きますけれども、解散命令請求の根拠として文化庁が悪質性や継続性を認めた民事判決三十二件のうち、既に大半の二十七件もの判決が出ていたにもかかわらず、なぜ二〇一五年八月には名称変更を認めたんですか。次長、お答えいただけますか。
        """

    # texts.append((convert(text, None), {1: 3}))
    # text = "地方行政・警察委員会について"
    # text = "4条の1の2と3、それと2の6ですね、これは憲法9条ですが、そして5条の7"
    # texts.append((convert(text, None), {1: 3}))
    #  texts = [convert(text, None)] * 100
    # start = time.perf_counter_ns()
    # list(nlp.pipe(texts=[(convert(text, None), {
    #     1: 3}, )] * 200, n_process=1, batch_size=10, as_tuples=True))
    # list(nlp.pipe(texts, n_process=4))

    # print((time.perf_counter_ns() - start) / 10 ** 9)
    nlp(text)
    return
    docs = nlp.pipe(
        [convert(text, None)], n_process=3, batch_size=10)
    # docs = nlp.pipe(
    #    [convert(text, None)])

    # print(time.perf_counter() - start)
    main_tokens_norms = []

    sub_tokens_norms = []

    for doc in docs:

        for sent in doc.sents:

            for t in sent:
                if t.dep_ == "nsubj":
                    print(t.i, t.lemma_)

            print(sent.vector_norm)
            for token in ginza.bunsetu_head_tokens(sent):
                print(token.lemma_, list(token.ancestors))

        for chunk in doc.noun_chunks:
            print(chunk.vector_norm)
            print(chunk.text)

            # print(list(chunk.noun_chunks))
        print(nlp.batch_size)
        print(doc.sentiment)
        # print(doc.user_data["sub_tokens"])
        # print(dir(doc.user_data["sub_tokens"][1][0][0]))
        processed = set()
        """"
        for token in doc:
            if token in processed:
                continue

            subtree_set = set()
            subtree_list = list()
            is_subtree_exist = not not subtree_list 
            while is_subtree_exist:

                for subtoken in token.subtree:
                    if subtoken.head not in subtree_set:
                        for subtoken.head.subtree:
                            
                        subtree_list.extend(
                            t for t in subtoken.head.subtree if t not in subtree_set)
                        subtree_set.update(subtoken.head.subtree)

            print(token, subtree_list)
        """
        for sent in doc.sents:

            for token in sent:

                if token.vector_norm != 0:
                    if token.pos_ in MAIN_POS:
                        main_tokens_norms.append(token.vector_norm)
                    else:
                        sub_tokens_norms.append(token.vector_norm)

                print(
                    token.i,
                    token.orth_,
                    token.lemma_,
                    token.norm_,
                    token.morph.get("Reading"),
                    token.pos_,
                    token.morph.get("Inflection"),
                    token.tag_,
                    token.dep_,
                    token.head.i,
                    token.vector_norm,
                    list(token.ancestors),
                    list(token.children),


                    list(token.subtree)
                )

            print('EOS')
        break
    print('main', sum(main_tokens_norms) / len(main_tokens_norms))
    print('sub', sum(sub_tokens_norms) / len(sub_tokens_norms))


# nlp = loadnlp('ja_ginza')


class ExampleClass:
    def get_nlp(self):
        return loadnlp('ja_ginza')

    def exec(self, i):
        example(self.get_nlp())


class Caller:
    funcclass = ExampleClass()

    def exec(self, pool):
        imap = pool.imap_unordered(
            self.funcclass.exec, range(100), chunksize=10)
        list(imap)


def main():
    instance = ExampleClass()
    start = time.perf_counter_ns()
    caller = Caller()
    with Pool(4) as pool:
        caller.exec(pool)
        print((time.perf_counter_ns() - start) / 10 ** 9)
        caller.exec(pool)
        print((time.perf_counter_ns() - start) / 10 ** 9)
        """
        imap = pool.imap_unordered(instance.exec, range(100), chunksize=25)
        list(imap)

        print((time.perf_counter_ns() - start) / 10 ** 9)
        imap = pool.imap_unordered(instance.exec, range(100), chunksize=25)
        list(imap)
        print((time.perf_counter_ns() - start) / 10 ** 9)
        """

    # start = time.perf_counter_ns()
    # example(1)


if __name__ == '__main__':

    main()
