import random
#from alphabet2kana import a2k

dic_file = 'data/bep-eng.txt'
dict_eng_names2kana = {}
with open(dic_file, mode='r', encoding='utf-8') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        if i >= 6:
            line_list = line.replace('\n', '').split(' ')
            dict_eng_names2kana[line_list[0].lower()] = line_list[1]


def get_katakana_name(eng_name):
    eng_name_lower = eng_name.lower()
    
    if eng_name_lower in dict_eng_names2kana:
        
        name_kt = dict_eng_names2kana[eng_name_lower]
        name_kt = name_kt.replace("ッ","")
        #name_kt = name_kt.replace("ヴ","ブ") #kana_to_uppwerで変更しないと「ヴ」が生まれてしまった
        name_kt = kana_to_upper(name_kt) #大文字変換
        name_kt = delete_nobashibo(name_kt) #伸ばし棒を母音に変換、ンのあとのやつは削除
        
        
        return name_kt
    else:
        return None

def kana_to_upper(name_kana):
    characters = str.maketrans("ァィゥェォヵヶッャュョヮヴ","アイウエオカケツヤユヨワブ") #大文字変換
    return name_kana.translate(characters)

def delete_nobashibo(name_kana):
    
    for x in range(len(name_kana) - 1):
        kana_list = list(name_kana) #一度リスト化しないとエラー出る(stringの要素は直接指定できない)
        if (kana_list[x + 1]) == "ー":

            if (kana_list[x] in ["ア","カ","サ","タ","ナ","ハ","マ","ヤ","ラ","ワ","ガ","ザ","ダ","バ","パ"]):

                kana_list[x + 1] = "ア"
            elif (kana_list[x] in ["イ","キ","シ","チ","ニ","ヒ","ミ","リ","ギ","ジ","ヂ","ビ","パ"]):
                kana_list[x + 1] = "イ"
            elif (kana_list[x] in ["ウ","ク","ス","ツ","ヌ","フ","ム","ユ","ル","グ","ズ","ヅ","ブ","プ"]):
                kana_list[x + 1] = "ウ"
            elif (kana_list[x] in ["エ","ケ","セ","テ","ネ","ヘ","メ","レ","ゲ","ゼ","デ","ベ","ペ"]):
                kana_list[x + 1] = "エ"
            elif (kana_list[x] in ["オ","コ","ソ","ト","ノ","ホ","モ","ヨ","ロ","ヲ","ゴ","ゾ","ド","ボ","ポ"]):
                kana_list[x + 1] = "オ"
        name_kana = "".join(kana_list)
    return name_kana.replace('ー', '') #ンの後の伸ばし棒とかは消してから渡す

 
#<editor-fold desc="Description">
def get_random_eng_name_list(num):
    return random.sample(dict_eng_names2kana.keys(), num)