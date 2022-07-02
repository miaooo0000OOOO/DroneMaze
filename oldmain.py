import numpy as np
import cv2
from show_map import map_img

MAPPATH = "map.csv"

video = cv2.cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'MJPG'), 30, (300, 300))

def VariablePrint():
    currentBlockSearchResult, currentBlockSearchProgress, \
        endAction, lastBlockSearchResult,\
        searchAction,
    print("当前格子的搜索结果：" + str(currentBlockSearchResult))
    print("当前格子的搜索进程：" + str(currentBlockSearchProgress))
    print("结束动作：" + str(endAction))
    print("上一格的搜索结果：" + str(lastBlockSearchResult))
    print("搜索动作：" + str(searchAction))
    print("坐标：" + str(e.drone.pos))
    print("方向：" + str(e.drone.direction))
    print()

def updateAndShowMap():
    global img
    img = map_img(e.drone.pos, e.drone.direction)
    video.write(img)
    #cv2.imshow("img", img)
    #cv2.waitKey(100)

def turn(d):
    global e
    if d == "LEFT":
        e.drone.left()
    else:
        e.drone.right()

def backOneBlock(actionPerformed):
    global e
    if actionPerformed == 6:
        turn("right")
    elif actionPerformed == 4:
        print("B")
    elif actionPerformed == 2:
        turn("left")
    e.drone.back()
    

def init_action():
    global e,stack,searchAction
    e.drone.d(0)
    searchAction,stack = [], []
    searchAction.append("RIGHT")
    searchAction.append("RANGING")
    searchAction.append("LEFT")
    searchAction.append("RANGING")
    searchAction.append("LEFT")
    searchAction.append("RANGING")

def stackPop():
    global stack
    return stack.pop()

def stackPush(value):
    global stack
    stack.append(value)

def searchInOneBlock():
    global currentBlockSearchResult, currentBlockSearchProgress, \
        endAction, lastBlockSearchResult,\
        searchAction, stack, e
    currentBlockSearchProgress = stack[-1]
    endAction = False
    currentBlockSearchResult = "CONTINUESEARCH"
    while not((currentBlockSearchProgress == 7)or(endAction == True)):
        #VariablePrint()
        isblocked = e.droneisblocked()
        endAction = False
        if searchAction[currentBlockSearchProgress-1] == "RANGING":
            if isblocked == False:
                e.drone.forward()
                stack[-1] = currentBlockSearchProgress
                if e.drone.pos == endPos:
                    currentBlockSearchResult = "END"
                else:
                    currentBlockSearchResult = "CONTINUESEARCH"
                    stackPush(1)
                endAction = True
        else:
            turn(searchAction[currentBlockSearchProgress-1])
        currentBlockSearchProgress += 1
        updateAndShowMap()
    if currentBlockSearchProgress == 7 and endAction == False:
        currentBlockSearchResult = "DEADEND"
        backOneBlock(6) # turn right and back
        stackPop()
        stack[-1] += 1
    lastBlockSearchResult = currentBlockSearchResult

def csvpos2mappos(csvpos):
    mappos = [(csvpos[0]-1)/2, (csvpos[1]-1)/2]
    return mappos

def mappos2csvpos(mappos):
    csvpos = [mappos[0]*2+1, mappos[1]*2+1]
    return csvpos

def mappos2realpos(mappos):
    realpos = [60*(mappos[0]-2),-60*(mappos[1]-2)]
    return realpos

def read_map(filename="map.csv"):
    h=open(filename)
    H=h.read()
    Hh=H.split("\n")
    data=[]
    for row in Hh:
        data.append(row.split(","))
    return data

class Drone:
    def __init__(self, pos, direction):
        self.pos = pos
        self.direction = direction
        self.backBlock = 0
    
    def forward(self):
        if self.direction == 0:
            self.pos[1]-=1
        elif self.direction == 1:
            self.pos[0]+=1
        elif self.direction == 2:
            self.pos[1]+=1
        elif self.direction == 3:
            self.pos[0]-=1
        #self.gotoxy(self.pos)
    
    def back(self):
        if self.direction == 0:
            self.pos[1]+=1
        elif self.direction == 1:
            self.pos[0]-=1
        elif self.direction == 2:
            self.pos[1]-=1
        elif self.direction == 3:
            self.pos[0]+=1
    
    # def d(self, direction):
    #     if direction in [0,1,2,3]:
    #         self.direction = direction
    #     else:
    #         raise ValueError("direction must be one of [0,1,2,3]")
    
    def right(self):
        self.direction = (self.direction+1)%4
        #self.drone.right()
    
    def left(self):
        self.direction = (self.direction-1)%4
        #self.drone.left()

    def toPos(self):
        if self.direction == 0:
            self.pos[1] += self.backBlock
        elif self.direction == 1:
            self.pos[0] -= self.backBlock
        elif self.direction == 2:
            self.pos[1] -= self.backBlock
        elif self.direction == 3:
            self.pos[0] += self.backBlock
        self.backBlock = 0

    def gotoxy(self, pos):
        if (pos[0]>=0 and pos[0]<=4)and(pos[1]>=0 and pos[1]<=4)and(pos[0]==int(pos[0]))and(pos[1]==int(pos[1])):
            self.pos = pos
        else:
            raise ValueError("pos must be integer between 0 and 4")

class Map():
    def __init__(self, mArray):
        self.mArray = mArray


class Env():
    def __init__(self):
        self.drone = Drone(pos=[2,4], direction = 0)
        self.map = Map(mArray=read_map())
    
    def droneisblocked(self):
        pos = mappos2csvpos(self.drone.pos)
        direction = self.drone.direction
        if direction == 0:
            pos[1]-=1
        elif direction == 1:
            pos[0]+=1
        elif direction == 2:
            pos[1]+=1
        elif direction == 3:
            pos[0]-=1
        #print(pos)
        return self.map.mArray[pos[1]][pos[0]] in ('1', '0')

e = Env()
img = map_img(e.drone.pos, e.drone.direction)
# cv2.imshow("img", img)
# cv2.waitKey(1000)
step = 0
endPos = [2, 0]
#defVar#
lastBlockSearchResult = "CONTINUESEARCH"#上一个格子的搜索结论
currentBlockSearchProgress = 0#当前格子的搜索进度
endAction = False#结束动作
currentBlockSearchResult = "CONTINUESEARCH"#当前格子的搜索结论
#defList#
searchAction = []#搜索动作
stack = []
init_action()
stack.append(1)
#探索
while not(lastBlockSearchResult == "END"):
    searchInOneBlock()
    img = map_img(e.drone.pos, e.drone.direction)
    step += 1
    # print(step)
#返回
print(stack)

backAction = []
s = stack.copy()
while(len(s)!=0):
    pop = s[-1]
    s.pop()
    backAction.insert(0,"B")
    if pop == 6:
        backAction.insert(0,"R")
    elif pop == 2:
        backAction.insert(0,"L")
print(backAction)


while e.drone.pos != [2, 4]:
    if len(backAction) == 0:
        e.drone.toPos()
    else:
        popBack = backAction.pop()
        if popBack =="B":
            e.drone.backBlock += 1
        elif popBack == "R":
            e.drone.toPos()
            e.drone.right()
        elif popBack == "L":
            e.drone.toPos()
            e.drone.left()
    updateAndShowMap()

"""
while e.drone.pos != [2, 4]:
    e.drone.forward()
    if stack[-1] == 6:
        e.drone.right()
    if stack[-1] == 2:
        e.drone.left()
    stack.pop()
    updateAndShowMap()
"""
video.release()
print("end")