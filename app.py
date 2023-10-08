from flask import Flask, redirect, request
from flask import render_template, send_file
from flask import json
import os
import re

import converter
import google_trans
import kana2kanji
import renderer
import dev_name_sample

#import english_to_kana
#import alkana
import unicodedata

app = Flask(__name__)

name_input_eng = ""
name_eng_lower = ""
name_kt = ""
name_kt_list = list() #["サン","テ", "ア","ゴ"]
name_kanji_list = list() #["参","手","亜","語"]
kanji_image_name = ""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate", methods=['POST'])
def generate_kanji_name():
    name_input_eng = request.form.get('myname','')
    frame_style = request.form.get('framestyle','')
    font_name = request.form.get('fontname','')
    font_color = request.form.get('fontcolor','')
    kanji_name = request.form.get('kanji_name', '')
    suggestions = request.form.get('suggestions', '')

    
    if suggestions:
        try:
            suggestions = eval(suggestions)
            suggestions.remove(kanji_name)
            if not len(suggestions):
                suggestions = ''
        except Exception as e:
            print(e)
            suggestions = ''

    print(kanji_name, type(suggestions))

    kanji_name_list = list() #候補一覧 (kanji_nameがある時は、もう表示しない)

    #if suggestions:
    #    kanji_name_list = suggestions

    name_input_eng = name_input_eng.rstrip()

    if not kanji_name:
        #img_type = request.form.get('img_type', 'sakura')
        if (name_input_eng == ''): return error_msg("Input your name and try again!")

        unicodedata.normalize("NFKC", name_input_eng) #正規化
        
        if (" " in name_input_eng) or ("\n" in name_input_eng):
            return error_msg("Please do not include any spaces in your name.")
            
        if not re.fullmatch('[a-zA-Z]+', name_input_eng):
            return error_msg("You can input only English Alphabets!")
        
        name_eng_lower = name_input_eng.lower()
        name_kt = converter.get_katakana_name(name_eng_lower)
        if name_kt == None or "":
            #print("Trying Google Translation")
            name_kt = google_trans.try_get_google_translated_name(name_eng_lower.capitalize())
            #最初を大文字にして渡している
            if name_kt is None or "":
                #print(f"Couldn't get {name_eng_lower}'s translation from Google Trans")
                return error_msg("Sorry, your name is not found on our dictionary")
        #この時点でもう小文字なし・伸ばし棒変換後
        #print(name_kt)
        
        for x in range(5):
            kanji_name = "".join(kana2kanji.get_kana2kanji_list(name_kt)) #漢字のリストを取得,漢字が"明日"のような2文字もあるのに注意
            if kanji_name not in kanji_name_list:
                kanji_name_list.append(kanji_name)

        kanji_name = kanji_name_list.pop(0)
    
    kanji_image_name = renderer.render_kanji(kanji_name, frame_style=frame_style, font_name=font_name, font_color=font_color)
    while not os.path.isfile(f"static/user_images/{kanji_image_name}.png"):
        #print("waiting for file")
        None
    return render_template("kanji_image.html",
        img_name=kanji_image_name,
        eng_name=name_input_eng,
        frame_style=frame_style,
        font_name=font_name,
        font_color=font_color,
        kanji_name=kanji_name,
        kanji_name_suggestions=suggestions if suggestions else kanji_name_list)
    

@app.route("/generate")
def redirect_index():
    return redirect('http://127.0.0.1:4999')

@app.route("/s")
def share():
    img_name = request.args.get('img')
    eng_name = request.args.get('name')
    if (not img_name) or (not eng_name):
        return redirect('http://127.0.0.1:4999')
    return render_template("share.html", img_name=img_name, eng_name=eng_name)
def error_msg(msg):
    return render_template("error.html",msg=msg)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=4999,debug=True)

"""
random_name_list = list()
#random_name_list = converter.get_random_eng_name_list(10)
for x in dev_name_sample.get_random_eng_names(100):
    y = converter.get_katakana_name(x)
    if (y is None or ""): y = google_trans.try_get_google_translated_name(x.capitalize())
    if (y is None or ""): 
        print(f"Can't translate: {x}")
        break
    else:
        show = "".join(kana2kanji.get_kana2kanji_list(y))
        print(f"{x}: {show}")
        renderer.render_kanji("".join(show))  #写真を作成
"""











