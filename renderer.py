from email.mime import image
import string
from PIL import Image, ImageDraw, ImageFont
import random
import uuid


path_font = "fonts/tamanegi-kaisho.ttf"
base_font_size = 260
font_size = 100
text_color = (0, 0, 0)
left_distance = 90

wrapping_image_root = "data/src/wrapping_images/"

def render_kanji(name_kanji_string, frame_style="sakura", font_name="tamanegi-kaisho", font_color="black"):
    
    font_size = base_font_size - len(name_kanji_string) * 21

    img = Image.open('data/src/kakizome_base.png') #512x1000
    img.putalpha(255)
    text = insert_line(name_kanji_string)
    #print(text)
    #print(img.format, img.size, img.mode)
    draw = ImageDraw.Draw(img)

    path_font = f"fonts/{font_name}.ttf"
    
    font = ImageFont.truetype(path_font, font_size)

    textWidth, textHeight = draw.textsize(text,font=font)

    
    textTopLeft = (180, img.size[1]//2) # 前から1/6，上下中央に配置、anchor='mm'
    draw.text(textTopLeft, text, fill=font_color, font=font, anchor="mm")
    
    wrapping_img = Image.open(wrapping_image_root + frame_style + ".png") #装飾用
    wrapping_img.convert("RGBA")
    #wrapping_img.putalpha(255)
    img = overlap_images(img, wrapping_img)

    draw2 =ImageDraw.Draw(img)
    font2 = ImageFont.truetype(path_font,45)
    color2 = "navy"
    if frame_style == "nami":
        color2 = "#ffb6c1"
    else:
        color2 = "navy"
    draw2.text((350, 950), "KanjiNinja.com", fill=color2, font=font2, anchor="mm")

    #draw.multiline_text((120,20), name_kanji_string, spacing=24, font=font, fill=(0,0,0,255), direction="ttb")

    
    img_name = str(uuid.uuid4())
    img_path = f"static/user_images/{img_name}.png"
    img.save(img_path)
    return img_name

def insert_line(name_kanji_string):
    
    new_text = ""
    for x in range(len(name_kanji_string)):
        new_text += name_kanji_string[x] #漢字を入れる
        if (x == len(name_kanji_string) - 1): #最後の文字なら改行しない
            break
        new_text += "\n"
    return new_text

def overlap_images(img_below, img_above):
    overlapped_img = Image.alpha_composite(img_below,img_above)
    #img_below.alpha_composite(img_above)
    #return img_below
    return overlapped_img
    

