import pandas as pd
import numpy as np
import random

dict_kana_kanji = dict()

max_kana_kanji_pair_count = 10 #Excelにおけるkanaを除いたcolumnの数

kana_2char_list = list() #keyのうち、カイのように二文字のもの
kana_1char_list = list() #keyのうち、サのように1文字のもの


def load_dict_and_kana():
    sheet_list = ["kana-kanji-sheet"]
    df = pd.read_excel("data/files/kana-kanji-data.xlsx", engine='openpyxl')
    for sheet_name in sheet_list:
        
        
        pair_list = df.to_dict(orient="records")
        
        pair_list_dict = pair_list 
        
        for pair in pair_list_dict:
            
            dict_kana_kanji[pair["kana"]] = list()
            if len(pair["kana"]) == 2:
                kana_2char_list.append(pair["kana"])
            else:
                kana_1char_list.append(pair["kana"])
            for x in range(0, max_kana_kanji_pair_count): #"kanji-" + str(0 ~ 9) #string型がkeyじゃないといけないのでkanji-とつけた
                
                keyX = "kanji-" + str(x)
                
                if not (pair[keyX] is np.NaN): #nullチェック
                    dict_kana_kanji[pair["kana"]].append(pair[keyX])
  
        



def split_kana(name_string):

    load_dict_and_kana() #dictionaryをロード

    
    split_kana_list = list()
    randomized_kana_2char_list = random.sample(kana_2char_list, len(kana_2char_list))
    
    

    while len(name_string) >= 2:
        for kana_2char in randomized_kana_2char_list: #2charをシャッフルして
            if len(name_string) < 2: break

            if (name_string[0] + name_string[1] == kana_2char): #length of name_string greater than 1
                
                split_kana_list.append(kana_2char)
                name_string = name_string[2:]
               
        else:
            split_kana_list.append(name_string[0])
            name_string = name_string[1:]
        
    else:
        
        if (len(name_string) == 1):
            split_kana_list.append(name_string)
    #print(split_kana_list)
    return split_kana_list

def get_kanji_list(name_kana_list):
    
    
    name_kanji_list = list()
    
    for kt in name_kana_list:
        name_kanji_list.append(random.choice(dict_kana_kanji[kt]))
    return name_kanji_list

def get_kana2kanji_list(name_string):
    return get_kanji_list(split_kana(name_string))