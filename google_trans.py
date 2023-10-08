from googletrans import Translator

import converter
import re

def try_get_google_translated_name(name):
    tr = Translator()
    result = tr.translate(name, src="en", dest="ja").text
    if result is None or "": return None
    if is_all_katakana(result) == False: return None
    result.replace("ッ","")
    #result.replace("ヴ","ブ") kana_to_upperで駆除
    result = converter.kana_to_upper(result)
    result = converter.delete_nobashibo(result)
    #print("trans finish: " + result)
    return result


def is_all_katakana(value):
    return re.match(r'^[\u30A0-\u30FF]+$', value) is not None
def is_all_hiragana(value):
    return re.match(r'^[\u3040-\u309F]+$', value) is not None

