#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Mario Chen, 11.02.2022, Shenzhen
# My Github site: https://github.com/Mario-Hero
import os

import random
import math
import win32gui
import numpy as np

try:
    import tkinter
except ImportError:
    os.system('pip install tkinter')
    import tkinter

try:
    from PIL import ImageGrab,Image,ImageTk
except ImportError:
    os.system('pip install pillow')
    from PIL import ImageGrab,Image,ImageTk

try:
    import cv2 as cv
except ImportError:
    os.system('pip install cv2')
    import cv2 as cv

    




canvasWidth = 700  #显示分辨率X resolutionX to show
canvasHeight = canvasWidth #显示分辨率Y resolutionY to show
LARGER_FACTOR = 3 # 实际导出分辨率为显示分辨率的[LARGER_FACTOR]倍 resolution to export is [LARGER_FACTOR] times of resolution to show

COLOR_SET = []
COLOR_ALPHABET = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
SHADOW_COLOR = (0,0,0)
cvWidth = canvasWidth*LARGER_FACTOR
cvHeight = canvasHeight*LARGER_FACTOR
shadowXY = (0,0)

def processKeyboardEvent(ke):
    #print("ke.keysym", ke.keysym)  # 按键别名
    #print("ke.char", ke.char)  # 按键对应的字符
    #print("ke.keycode", ke.keycode)
    if ke.keysym == 'space':
        reDraw() # next picture
    elif ke.keysym == 's':
        saveCanvas() # save


def randomColor():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def randomDarkColor():
    return (random.randint(0, 128), random.randint(0, 128), random.randint(0, 128))

def randomThickness():
    return random.randint(1, int(cvWidth/20))


def randomRectangle():
    x1 = random.randrange(cvWidth)
    y1 = random.randrange(cvHeight)
    x2 = x1 + random.randrange(cvWidth)
    y2 = y1 + random.randrange(cvHeight)
    if randBoolean():
        color = randomColor()
        t = randomThickness()
        if randBoolean():
            cv.rectangle(im, shadowAdd(x1 - t, y1 - t), shadowAdd(x1 + t, y2 + t), SHADOW_COLOR, cv.FILLED)
            cv.rectangle(im, shadowAdd(x1 - t, y1 - t), shadowAdd(x2 + t, y1 + t), SHADOW_COLOR, cv.FILLED)
            cv.rectangle(im, shadowAdd(x2 + t, y2 + t), shadowAdd(x2 - t, y1 - t), SHADOW_COLOR, cv.FILLED)
            cv.rectangle(im, shadowAdd(x2 + t, y2 + t), shadowAdd(x1 - t, y2 - t), SHADOW_COLOR, cv.FILLED)
        cv.rectangle(im, (x1-t, y1-t), (x1+t, y2+t), color, cv.FILLED)
        cv.rectangle(im, (x1-t, y1-t), (x2+t, y1+t), color, cv.FILLED)
        cv.rectangle(im, (x2+t, y2+t), (x2-t, y1-t), color, cv.FILLED)
        cv.rectangle(im, (x2+t, y2+t), (x1-t, y2-t), color, cv.FILLED)
    else:
        if randBoolean():
            cv.rectangle(im, shadowAdd(x1, y1), shadowAdd(x2, y2), SHADOW_COLOR, cv.FILLED)
        cv.rectangle(im, (x1, y1), (x2, y2), randomColor(),cv.FILLED)


def randomPolygon():
    points = []
    for i in range(random.randint(3,8)):
        x = random.randrange(cvWidth)
        y = random.randrange(cvHeight)
        points.append([x,y])
    pointNumpy = np.array(points,dtype=np.int32)
    if randBoolean():
        cv.polylines(im,[pointNumpy],1,randomColor(),int(randomThickness()/4),cv.LINE_AA)
    else:
        lightIm = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
        cv.polylines(lightIm, [pointNumpy], 1, randomColor(), int(randomThickness() / 4), cv.LINE_AA)
        if randBoolean():
            cv.subtract(im, lightIm, im)
        else:
            cv.add(im, lightIm, im)


def randomShadow():
    global shadowXY, SHADOW_COLOR
    r = randomThickness()
    x = random.randrange(-r,r)
    y = random.randrange(-r, r)
    shadowXY = (x, y)
    SHADOW_COLOR = randomDarkColor()


def shadowAdd(x,y):
    return (shadowXY[0]+x, shadowXY[1]+y)


def randomCircle():
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    r = int(random.randrange(cvWidth)/5)
    w = random.randint(5,int(cvWidth/10))
    if randBoolean():
        if randBoolean():
            cv.circle(im, shadowAdd(x, y), r, SHADOW_COLOR, w, cv.LINE_AA)
        cv.circle(im, (x,y), r, randomColor(), w, cv.LINE_AA)
    else:
        if randBoolean():
            cv.circle(im, shadowAdd(x, y), r, SHADOW_COLOR, cv.FILLED)
            cv.circle(im, (x, y), r, randomColor(), cv.FILLED)
        else:
            if randBoolean():
                lightIm = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
                cv.circle(lightIm, (x, y), r, randomColor(), cv.FILLED)
                if randBoolean():
                    cv.subtract(im,lightIm,im)
                else:
                    cv.add(im,lightIm,im)
            else:
                cv.circle(im, (x, y), r, randomColor(), cv.FILLED)


def randBoolean():
    return random.choice([True, False])


def randomStackCircle():
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    r = int(random.randrange(cvWidth) / 10)
    t = random.randint(1, 5)
    dx = int(random.randrange(cvWidth) / 20 ) * random.choice([-1, 1])
    dy = int(random.randrange(cvHeight) / 20 ) * random.choice([-1, 1])
    dr = int(random.randrange(cvWidth) / 30)
    for i in range(t):
        cv.circle(im, (x+i*dx, y+i*dy), r + i*dr, randomColor(), cv.FILLED)


def randomStackCircle2():
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    r = int(random.randrange(cvWidth) / 10)
    t = random.randint(1, 20)
    dr = int(random.randrange(cvWidth) / 20)
    for i in range(t-1,-1,-1):
        cv.circle(im, (x, y), r + i*dr, randomColor(), cv.FILLED)


def randomStackRectangle():
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    w1 = int(random.randrange(cvWidth) / 10)
    w2 = int(random.randrange(cvWidth) / 15)
    h = int(random.randrange(cvHeight)/2)
    fillColor = randomColor()
    if randBoolean():
        for i in range(random.randint(3, 8)):
            cv.rectangle(im, (int(x + i * (w1+w2)), y), (x + i * (w1+w2) + w1, y + h), fillColor, -1)
    else:
        thickness = int(randomThickness()/5)
        for i in range(random.randint(3, 8)):
            cv.rectangle(im, (int(x + i * (w1+w2)), y), (x + i * (w1+w2) + w1, y + h), fillColor, thickness,cv.LINE_AA)


def randomSquareRotate():
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    w = int(random.randrange(cvWidth) / 10)
    rad = random.randrange(90)
    squareRotate(x,y,w,rad,randomColor(), width=random.randint(0, int(x/10)))


def squareRotate(x,y,w,rad=45,color=(0,0,0),width=0):
    a=math.pi*rad/180
    coord = [[x - w * math.sin(a)/math.sqrt(2),y - w * math.cos(a)/math.sqrt(2)],
              [x + w * math.cos(a)/math.sqrt(2),y - w * math.sin(a)/math.sqrt(2)],
               [x + w * math.sin(a)/math.sqrt(2),y + w * math.cos(a)/math.sqrt(2)],
                [x - w * math.cos(a)/math.sqrt(2),y + w * math.sin(a)/math.sqrt(2)]]
    pointNumpy = np.array(coord, dtype=np.int32)
    if randBoolean():
        cv.polylines(im,[pointNumpy],1,color,int(randomThickness()/4),cv.LINE_AA)
    else:
        lightIm = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
        cv.polylines(lightIm, [pointNumpy], 1, color, int(randomThickness() / 4), cv.LINE_AA)
        if randBoolean():
            cv.subtract(im, lightIm, im)
        else:
            cv.add(im, lightIm, im)


def randomArc():
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    r = int(random.randrange(cvWidth) / 10)
    rad = random.randrange(360)
    if randBoolean():
        cv.ellipse(im, (x, y), (r, r), 0, 0, rad, randomColor(),cv.FILLED)
    else:
        cv.ellipse(im, (x, y), (r, r), 0, 0, rad, randomColor(),int(randomThickness()/10),cv.LINE_AA)


def randomLine():
    x1 = random.randrange(cvWidth)
    y1 = random.randrange(cvHeight)
    x2 = random.randrange(cvWidth)
    y2 = random.randrange(cvHeight)
    if randBoolean():
        lightIm = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
        cv.line(lightIm,(x1,y1),(x2,y2),randomColor(),randomThickness(),cv.LINE_AA)
        if randBoolean():
            cv.subtract(im, lightIm, im)
        else:
            cv.add(im, lightIm, im)
    else:
        cv.line(im, (x1, y1), (x2, y2), randomColor(), randomThickness(), cv.LINE_AA)


def showPic():
    global imgTK, im
    imgCV2 = cv.cvtColor(im, cv.COLOR_BGR2RGBA)  # 转换颜色从BGR到RGBA
    current_image = Image.fromarray(imgCV2)  # 将图像转换成Image对象
    current_image = current_image.resize((canvasWidth,canvasHeight),Image.ANTIALIAS)
    imgTK = ImageTk.PhotoImage(image=current_image)  # 将image对象转换为imageTK对象
    canvas.create_image(0, 0, anchor='nw', image=imgTK)


def randomDarkCircle():
    global im
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    r = int(random.randrange(cvWidth) / 3)
    lightIm = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
    for i in range(x-r,x+r):
        for j in range(y-r,y+r):
            if i > 0 and i < cvWidth and j > 0 and j < cvHeight:
                k = (i - x)*(i - x) + (j-y)*(j-y)
                if k <= r*r:
                    lightIm[i][j] = int(120 * (1-k/(r*r)))
    cv.subtract(im,lightIm,im)


def randomLightCircle():
    global im
    x = random.randrange(cvWidth)
    y = random.randrange(cvHeight)
    r = int(random.randrange(cvWidth) / 3)
    lightIm = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
    for i in range(x-r,x+r):
        for j in range(y-r,y+r):
            if i > 0 and i < cvWidth and j > 0 and j < cvHeight:
                k = (i - x)*(i - x) + (j-y)*(j-y)
                if k <= r*r:
                    lightIm[i][j] = int(120 * (1-k/(r*r)))
    cv.add(im,lightIm,im)


def reDraw():
    global imgTK, im
    randomShadow()
    canvas.delete(tkinter.ALL)
    canvas.create_rectangle(0,0,canvasWidth,canvasHeight,fill='black',width=0)
    im = np.zeros((cvWidth, cvHeight, 3), dtype=np.uint8)
    backGroundColor = randomColor()
    cv.rectangle(im,(0,0),(cvWidth,cvHeight),backGroundColor,cv.FILLED)
    '''
    for i in range(cvWidth):
        for j in range(cvHeight):
            im[i][j] = backGroundColor
            '''
    '''
    for i in range(random.randint(0, 1)):
        if randBoolean():
            randomStackCircle()
        else:
            randomStackCircle2()
            '''
    for i in range(random.randint(0, 5)):
        randomCircle()
    for i in range(random.randint(0, 5)):
        randomRectangle()
    for i in range(random.randint(0, 2)):
        randomPolygon()
    for i in range(random.randint(0, 2)):
        randomStackRectangle()
    for i in range(random.randint(0, 3)):
        randomSquareRotate()
    '''
    for i in range(random.randint(0, 3)):
        randomArc()
        '''
    for i in range(random.randint(0, 0)):
        randomLine()

    '''
    for i in range(random.randint(0, 2)):
        randomLightCircle()
    for i in range(random.randint(0, 2)):
        randomDarkCircle()
        '''
    showPic()


def saveCanvas():
    savePath = os.path.join(os.getcwd(),'pic-0.jpg')
    i = 0
    while os.path.exists(savePath):
        savePath = os.path.join(os.getcwd(),'pic-' + str(i) + '.jpg')
        i += 1
    cv.imwrite(savePath, im)

if __name__ == '__main__':
    tk = tkinter.Tk()
    canvas = tkinter.Canvas(tk, width=canvasWidth, height=canvasHeight, bg='white')
    canvas.pack()
    canvas.focus_set()
    canvas.bind(sequence="<Key>", func=processKeyboardEvent)
    reDraw()
    #canvas.create_line(0, 0, 500, 500)
    tk.mainloop()
