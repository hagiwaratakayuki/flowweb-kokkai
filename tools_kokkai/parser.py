import re
import json
from collections import defaultdict
略称が含まれる行を表す正規表現 = re.compile("^(明治|大正|昭和|平成|令和)[^（]+\s", re.U)
空白を表す正規表現 = re.compile("\s+", re.U)
間違っている略称のリスト = ["保安四法", "中央省庁等改革関連法", "組織犯罪対策三法"]


with open("./rows.txt", mode="r", encoding="utf-8") as fp:

    正式名称 = ""
    略称と正式名称の対応表 = {
        "AV新法": "性をめぐる個人の尊厳が重んぜられる社会の形成に資するために性行為映像制作物への出演に係る被害の防止を図り及び出演者の救済に資するための出演契約等に関する特則等に関する法律",
        "AV新法施行規則": "性をめぐる個人の尊厳が重んぜられる社会の形成に資するために性行為映像制作物への出演に係る被害の防止を図り及び出演者の救済に資するための出演契約等に関する特則等に関する法律施行規則",
        "保安四法": "保安四法",
        "刑法": "刑法",
        "アイヌ文化振興法": "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律",
        "アイヌ文化法": "アイヌ文化の振興並びにアイヌの伝統等に関する知識の普及及び啓発に関する法律",
        "中央省庁等改革関連法": "中央省庁等改革関連法",
        "組織犯罪対策三法": "組織犯罪対策三法",
        "高プロ": "高度プロフェッショナル制度"
    }
    for 行 in fp.read().replace("抄", "").strip().splitlines():
        if 略称が含まれる行を表す正規表現.search(行) is None:
            正式名称 += 行
        else:
            略称リスト = 空白を表す正規表現.split(行)[1:]
            for 略称 in 略称リスト:
                if 略称 == "":
                    continue
                if 略称 in 間違っている略称のリスト and len(略称リスト) == 1:

                    略称 = 正式名称

                略称と正式名称の対応表[略称] = 正式名称

            正式名称 = ""
略称の転置インデックス = defaultdict(set)


def custom(v):
    if isinstance(v, set):
        return list(v)
    return v


for 略称 in 略称と正式名称の対応表.keys():
    リスト化した略称 = [略称]
    for 開始地点 in range(len(略称) - 1):
        キー = 略称[開始地点:開始地点+2]
        略称の転置インデックス[キー].update(リスト化した略称)
with open("../processer/doc2vec/tokenaizer/japanese_language/kokkai_specificword/ryakusyou_tenchi.json", mode="w", encoding="utf-8") as fp:
    json.dump(obj=略称の転置インデックス, fp=fp, ensure_ascii=False, default=custom)
with open("../processer/doc2vec/tokenaizer/japanese_language/kokkai_specificword/ryakusyou.json", mode="w", encoding="utf-8") as fp:
    json.dump(obj=略称と正式名称の対応表, fp=fp, ensure_ascii=False, default=custom)
