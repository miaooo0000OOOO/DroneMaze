import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


def cv2ImgAddText(img, text, left, top, textColor=(0, 255, 0), textSize=20):
    if (isinstance(img, np.ndarray)): # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    fontStyle = ImageFont.truetype(
        "font/simsun.ttc", textSize, encoding="utf-8")
    # 绘制文本
    draw.text((left, top), text, textColor, font=fontStyle)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

def mappos2realpos(mappos):
    realpos = [60*(mappos[0]-2),-60*(mappos[1]-2)]
    return realpos

def show(x,y,a,b, img):
    if b==0:
        color=(255,255,255) #G
    elif b==1:
        color=(0,0,255) #R
    elif b==2:
        color=(0,255,0) #B
    else:
        color=(255,0,0)
    if a==0:
        cv2.rectangle(img,(x*60,y*60+5),(x*60+4,y*60+54),color,-1)
    elif a==1:
        cv2.rectangle(img,(x*60+5,y*60+55),(x*60+54,y*60+59),color,-1)
    elif a==2:
        cv2.rectangle(img,(x*60+55,y*60+5),(x*60+59,y*60+54),color,-1)
    elif a==3:
        cv2.rectangle(img,(x*60+5,y*60),(x*60+54,y*60+4),color,-1)
    else:
        cv2.circle(img,(x*60+30,y*60+30),20,color,-1)
    return img
 

def read_map(filename="map.csv"):
    h=open(filename)
    H=h.read()
    Hh=H.split("\n")
    data=[]
    for row in Hh:
        data.append(row.split(","))
    h.close()
    return data

def map_img(drone_pos, direction, map_data=read_map()):
    img = img=np.ones((300,300,3),np.uint8)*255
    
    ## 生成img
    # 墙和识别卡
    for x in range(5):
        for y in range(5):
            show(x,y,0,int(map_data[2*y+1][2*x]), img)
            show(x,y,1,int(map_data[2*y+2][2*x+1]), img)
            show(x,y,2,int(map_data[2*y+1][2*x+2]), img)
            show(x,y,3,int(map_data[2*y][2*x+1]), img)
            show(x,y,4,int(map_data[2*y+1][2*x+1]), img)
    # 无人机

    #cv2.circle(img, (drone_pos[0]*60+30, drone_pos[1]*60+30), 10, (0,0,0), -1)
    DTEXT = "上右下左"
    #cv2.putText(img, DTEXT[direction], (drone_pos[0]*60+30, drone_pos[1]*60+30), cv2.FONT_HERSHEY_PLAIN, 2.0, (0, 0, 255), 2)
    pos = drone_pos[0]*60+30, drone_pos[1]*60+30
    textSize = 50
    # img = cv2ImgAddText(img, DTEXT[direction], pos[0]-textSize/2, pos[1]-textSize/2, textColor=(48,30,216), textSize=textSize
    img = cv2ImgAddText(img, DTEXT[direction], pos[0]-textSize/2, pos[1]-textSize/2, textColor=(0,0,0), textSize=textSize)
    return img

if __name__ == '__main__':
    I = map_img((2,4), 3)
    cv2.imshow("img", I)
    cv2.waitKey(0)