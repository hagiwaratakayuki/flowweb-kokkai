import re
import json
from collections import defaultdict
import unicodedata
略称が含まれる行を表す正規表現 = re.compile(r"^(明治|大正|昭和|平成|令和)[^（]+\s", re.U)
空白を表す正規表現 = re.compile(r"\s+", re.U)
間違っている略称のリスト = ["保安四法", "中央省庁等改革関連法", "組織犯罪対策三法"]
活火山法の略称 = re.compile('活動?火山法')
特措法 = "特措法"
特法 = "特法"


def custom(v):
    if isinstance(v, set):
        return list(v)
    return v


def reguraize(name: str):
    ret = [name]
    if 特法 in name:
        ret.append(name.replace(特法, 特措法))
    if 特措法 in name:
        ret.append(name.replace(特措法, 特法))
    return ret


with open("./law.txt", mode="r", encoding="utf-8") as fp:

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
        "BSE特措法": "牛海綿状脳症対策特別措置法",
        "憲法": "日本国憲法",
        "同和立法": "同和対策事業特別措置法",
        "地対法": "地域改善対策特別措置法",
        "地対財特法": "地域改善対策特定事業に係る国の財政上の特別措置に関する法律",
        "スマホソフトウェア競争促進法": "スマートフォンにおいて利用される特定ソフトウェアに係る競争の促進に関する法律",
        "スマホソフト競争促進法": "スマートフォンにおいて利用される特定ソフトウェアに係る競争の促進に関する法律",
        "スマホ競争促進法": "スマートフォンにおいて利用される特定ソフトウェアに係る競争の促進に関する法律",
        "スマホ新法": "スマートフォンにおいて利用される特定ソフトウェアに係る競争の促進に関する法律",
        "巨大IT新法": "スマートフォンにおいて利用される特定ソフトウェアに係る競争の促進に関する法律"
    }
    全体 = unicodedata.normalize('NFKC', fp.read().replace("抄", "").strip())
    for 行 in 全体.splitlines():

        if 略称が含まれる行を表す正規表現.search(行) is None:
            正式名称 += 行
        else:
            略称リスト = 空白を表す正規表現.split(行)[1:]
            for 略称 in 略称リスト:
                if 略称 == "":
                    continue
                if 略称 in 間違っている略称のリスト and len(略称リスト) == 1:

                    略称 = 正式名称
                if 略称 == "アイヌ新法" or 活火山法の略称.search(略称) is not None:
                    continue
                正規化された略称のリスト = reguraize(略称)
                for 正規化された略称 in 正規化された略称のリスト:
                    略称と正式名称の対応表[正規化された略称] = 正式名称

            正式名称 = ""

with open("./horeibunko.text", mode="r", encoding="utf-8") as fp:
    正式名称のある行か判定するフラグ = True
    全体 = unicodedata.normalize('NFKC', fp.read().replace("抄", "").strip())
    for 行 in 全体.splitlines():
        if "索引" in 行 and '「' in 行:

            continue
        if 正式名称のある行か判定するフラグ and 略称 != "アイヌ新法" and 活火山法の略称.search(略称) is None:
            正式名称 = '　'.join(空白を表す正規表現.split(行)[:-1])
            正規化された略称のリスト = reguraize(略称)
            for 正規化された略称 in 正規化された略称のリスト:
                略称と正式名称の対応表[正規化された略称] = 正式名称
        else:

            略称 = 行.strip()
        正式名称のある行か判定するフラグ = not 正式名称のある行か判定するフラグ


略称の転置インデックス = defaultdict(set)


for 略称 in 略称と正式名称の対応表.keys():

    for 開始地点 in range(len(略称) - 1):
        トークン = 略称[開始地点:開始地点 + 2]
        if トークン in 特措法 or トークン in 特法:
            continue
        略称の転置インデックス[トークン].add(略称)
with open("../processer/doc2vec/tokenaizer/japanese_language/extracter/kokkai_specificword/ryakusyou_tenchi.json", mode="w", encoding="utf-8") as fp:
    json.dump(obj=略称の転置インデックス, fp=fp, ensure_ascii=False, default=custom)
with open("../processer/doc2vec/tokenaizer/japanese_language/extracter/kokkai_specificword/ryakusyou.json", mode="w", encoding="utf-8") as fp:
    json.dump(obj=略称と正式名称の対応表, fp=fp, ensure_ascii=False, default=custom)
