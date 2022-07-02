import cv2
import numpy as np
from show_map import map_img

EMPTY, CELL, WALL, CARD= 2, 0, 1, 3
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
RANGING = 2
ENDPOS = np.array([2, 0])
direction2vector = {UP:np.array([0,-1]), RIGHT:np.array([1,0]), DOWN:np.array([0,1]), LEFT:np.array([-1,0])}

class Map():
    def __init__(self):
        self.mArray = self.load_map()

    def load_map(self, filename="map.csv"):
        h=open(filename)
        H=h.read()
        Hh=H.split("\n")
        data=[]
        for row in Hh:
            if row=='':
                continue
            strlist = row.split(",")
            intlist=[int(strlist[i]) for i in range(len(strlist))]
            data.append(intlist)
        return data
    
    def mappos2mpos(self, pos):
        return 2*pos+1
    
    def isWall(self, pos, direction):
        mpos = self.mappos2mpos(pos)
        wallPos = mpos + direction2vector[direction]
        return self.mArray[wallPos[1]][wallPos[0]] == WALL

class Drone:
    def __init__(self, pos=np.array([2,4]), direction=0):
        self.pos = pos
        self.direction = direction

    def canMove(self, pos, direction, m:Map):
        posMoved = pos + direction2vector[direction]
        return not((pos == np.clip(posMoved, 0, 4)).all() or m.isWall(pos, direction))

    def renderFrame(self):
        global img, video
        img = map_img(self.pos, self.direction)
        video.write(img)
        cv2.imshow("img", img)
        cv2.waitKey(200)
        
    def forward(self, m:Map):
        if not self.canMove(self.pos, self.direction, m):
            raise
        self.pos += direction2vector[self.direction]
        self.renderFrame()

    def back(self, m:Map):
        d = (self.direction+2)%4
        if not self.canMove(self.pos, d, m):
            raise
        self.pos += direction2vector[d]
        self.renderFrame()

    def right(self):
        self.direction = (self.direction+1)%4
        self.renderFrame()
    
    def left(self):
        self.direction = (self.direction-1)%4
        self.renderFrame()

    def moveOneBlock(self, direction, m:Map):
        if not self.canMove(self.pos, direction, m):
            raise
        self.pos += direction2vector[direction]
        self.renderFrame()

    def move(self, direction, distance, m):
        for i in range(distance):
            self.moveOneBlock(direction, m)

    def ranging(self, m:Map):
        return m.isWall(self.pos, self.direction)

class Env():
    def __init__(self):
        self.drone = Drone()
        self.map = Map()
    def ranging(self):
        return self.drone.ranging(self.map)
    def left(self):
        self.drone.left()
    def right(self):
        self.drone.right()
    def turn(self, direction):
        if direction == RIGHT:
            self.right()
        else:
            self.left()
    def forward(self):
        self.drone.forward(self.map)
    def back(self):
        self.drone.back(self.map)
    def move(self, direction, distance):
        self.drone.move(direction, distance, self.map)
    def moveOneBlock(self, direction):
        self.drone.moveOneBlock(direction, self.map)

def searchInOneBlock():
    global e, stack, endSearch, searchProgress
    searchProgress = stack[-1]
    endAction = False
    while not(searchProgress==7 or endAction):
        endAction = False
        if actionOrder[searchProgress-1]==RANGING:
            isblocked = e.ranging()
            if not isblocked:
                e.forward()
                print(e.drone.pos)
                stack[-1] = searchProgress
                if (e.drone.pos == ENDPOS).all():
                    endSearch = True
                else:
                    stack.append(1)
                endAction = True
        else:
            e.turn(actionOrder[searchProgress-1])
        searchProgress += 1
    if searchProgress==7 and not endAction:
        e.right()
        e.back()
        stack.pop()
        stack[-1] += 1
    
if __name__ == '__main__':
    video = cv2.cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*'MJPG'), 30, (300, 300))
    e = Env()
    actionOrder = [RIGHT, RANGING, LEFT, RANGING, LEFT, RANGING]
    stack = []
    stack.append(1)
    endSearch = False
    e.drone.renderFrame()

    while not(endSearch):
        searchInOneBlock()
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

    backBlocks = 0
    d = (e.drone.direction+2)%4
    while (e.drone.pos != np.array([2, 4])).any():
        if len(backAction) == 0:
            e.move(d, backBlocks)
            backBlocks = 0
        else:
            popBack = backAction.pop()
            if popBack =="B":
                backBlocks += 1
            elif popBack == "R":
                e.move(d, backBlocks)
                backBlocks = 0
                d = (d+1)%4
            elif popBack == "L":
                e.move(d, backBlocks)
                backBlocks = 0
                d = (d-1)%4

    video.release()
    print("end")