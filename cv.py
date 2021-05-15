import cv2
import numpy as np
m=np.zeros((5,5,5),np.uint8)
img=np.ones((300,300,3),np.uint8)*255
def show(x,y,a,b, ifTZK):
    if b==0:
        color=(255,0,0) #B
    elif b==1:
        color=(0,255,0) #G
    else:
        color=(0,0,255) #R
    if ifTZK:
        cv2.circle(img,(x*60+30,y*60+30),20,color,-1)
    else:
        if a==0:
            cv2.rectangle(img,(x*60,y*60+5),(x*60+5,y*60+55),color,-1)
        elif a==1:
            cv2.rectangle(img,(x*60+5,y*60+55),(x*60+55,y*60+60),color,-1)
        elif a==2:
            cv2.rectangle(img,(x*60+55,y*60+5),(x*60+60,y*60+55),color,-1)
        elif a==3:
            cv2.rectangle(img,(x*60+5,y*60),(x*60+55,y*60+5),color,-1)


def write_map(m):
    for i in range(5):
        for j in range(5):
            for d in range(4):
                if m[j][i][d]==0:
                    show(j,i,d,1,True)

write_map(m)
cv2.imshow('img',img)
cv2.waitKey(0)