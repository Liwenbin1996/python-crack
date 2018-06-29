#-*- coding:utf8 -*-
from PIL import Image
import time
import os
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('file')
args = parser.parse_args()

IMG = args.file

"""
向量空间搜索引擎算法
"""
class VectorCompare:
    #计算矢量的模
    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.iteritems():
            total += count ** 2
        return math.sqrt(total)

    #计算矢量之间的cos值
    def relation(self, concordance1, concordance2):
        relevance = 0
        topvalue = 0
        for word, count in concordance1.iteritems():
            if concordance2.has_key(word):
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

#将图片转换为矢量
def buildVector(im):
    d1 = {}

    count = 0
    for i in im.getdata():
        d1[count] = i
        count += 1
    return d1

v = VectorCompare()

iconset = ['0', '1', '2', '3' ,'4' ,'5' ,'6' ,'7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

imageset = []

#加载训练集
im = Image.open(IMG)
im2 = Image.new("P",im.size,255)
for letter in iconset:
    for img in os.listdir('./iconset/%s/' % (letter)):
        if img != "Thumbs.db" and img != ".DS_Store":
            image = Image.open("./iconset/%s/%s"%(letter, img))
            image = buildVector(image)
            imageset.append({letter: image})


#将图片进行二值化，220和227是验证码中字符部分使用最多的像素点
for x in range(im.size[1]):
    for y in range(im.size[0]):
        pix  = im.getpixel((y, x))
        if pix == 220 or pix == 227:
            im2.putpixel((y,x), 0)
        else:
            im2.putpixel((y,x), 255)

im2.show()
inletter = False
foundletter = False
start = 0
end = 0

letters = []

#对验证码图片进行纵向分割
for y in range(im2.size[0]):
    for x in range(im2.size[1]):
        pix = im2.getpixel((y,x))
        if pix != 255:
            inletter = True
    
    if foundletter == False and inletter == True:
        foundletter = True
        start = y
    
    if foundletter == True and inletter == False:
        foundletter = False
        end = y
        letters.append((start, end))
    inletter = False

#count = 0

#对验证码图片进行分割
for letter in letters:
    im3 = im2.crop((letter[0], 0, letter[1], im2.size[1]))

    guess = []

    #与每个训练集中的图片进行对比，找到相似度最大的图片
    for image in imageset:
        for x,y in image.iteritems():
            guess.append((v.relation(y, buildVector(im3)), x))

    guess.sort(reverse=True)

    print "",guess[0]
