#coding:utf-8
import random
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np 

def randRGB():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def captcha_draw(label, fonts, dir_path):
    width, height = 768, 32
    size_cha = random.randint(24, 32) # 字符大小
    derx = random.randint(0, 10)
    im = Image.new(mode='L', size=(width, height), color='white') # color 背景颜色，size 图片大小
    drawer = ImageDraw.Draw(im)
    font = ImageFont.truetype(random.choice(fonts), size_cha)
    drawer.text(xy=(derx, 0), text=label, font=font, fill='black') #text 内容，font 字体（包括大小）
    # im.show()
    write2file(dir_path, label, im)

    
def write2file(dir_path, label, im):
    if os.path.exists(dir_path) == False: # 如果文件夹不存在，则创建对应的文件夹
        os.makedirs(dir_path)
        pic_id = 1
    else:
        pic_names = map(lambda x: x.split('.')[0], os.listdir(dir_path))
        pic_names.remove('label')
        pic_id = max(map(int, pic_names))+1 # 找到所有图片的最大标号，方便命名

    img_name = str(pic_id) + '.jpg'
    img_path = dir_path + img_name
    label_path = dir_path + 'label.txt'
    with open(label_path, 'a') as f:
        f.write((''.join(label)).encode('utf-8')) # 在label文件末尾添加新图片的text内容
    print img_path
    im.save(img_path)

if __name__ == "__main__":
    font_dir = 'fonts/'
    font_paths = map(lambda x: font_dir+x, os.listdir(font_dir))
    label_dir = 'TXT/'
    names = os.listdir(label_dir)
    max_len = 20
    cnt = 50000
    idx = 0
    for name in names:
        txt_path = label_dir+name 
        with open(txt_path) as f:
            for raw in f:
                raw = raw.decode('utf-8')
                if len(raw) <= 20:
                    captcha_draw(raw, font_paths, 'cv_data_%d/'%idx)
                    cnt -= 1
        if cnt < 0:
            cnt = 50000
            idx += 1