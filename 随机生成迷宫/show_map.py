import cv2
import numpy as np

L = IMGSIZE = 300
EMPTY, CELL, WALL, CARD= 2, 0, 1, 3
UP, RIGHT, DOWN, LEFT = 0, 1, 2, 3
HENG, SHU = 0, 1
BLACK, RED, BLUE = (0,0,0), (0,0,255), (255,0,0)
direction2vector = {UP:np.array([0,-1]), RIGHT:np.array([1,0]), DOWN:np.array([0,1]), LEFT:np.array([-1,0])}
direction2state = {UP:HENG, RIGHT:SHU, DOWN:HENG, LEFT:SHU}

class Map:
    def __init__(self):
        self.m = -np.ones((11,11))
        for y in range(1, 11, 2):
            for x in range(1, 11, 2):
                self.m[y, x] = CELL
        for y in range(0, 12, 2):
            for x in range(1, 11, 2):
                self.m[y, x] = WALL
        for y in range(1, 11, 2):
            for x in range(0 ,12, 2):
                self.m[y, x] = WALL
        self.reset_img()
    
    def reset_img(self):
        self.img = np.ones((IMGSIZE,IMGSIZE,3),np.uint8)*255

    def draw_wall(self, pos ,direction):
        imgPos = L/5*pos+L/10
        wImgPos = imgPos + L/10*direction2vector[direction]
        wState = direction2state[direction]
        if wState == HENG:
            wImgPos1 = wImgPos + L/10*direction2vector[LEFT]
            wImgPos2 = wImgPos + L/10*direction2vector[RIGHT]
        else: #SHU
            wImgPos1 = wImgPos + L/10*direction2vector[UP]
            wImgPos2 = wImgPos + L/10*direction2vector[DOWN]
        cv2.line(self.img, (int(wImgPos1[0]), int(wImgPos1[1])), (int(wImgPos2[0]), int(wImgPos2[1])), RED, cv2.LINE_4)

    def draw_card(self, pos):
        imgPos = L/5*pos+L/10
        cv2.circle(self.img, (int(imgPos[0]),int(imgPos[1])), int(L/14), BLUE, -1)

    def draw_map(self):
        for y in range(5):
            for x in range(5):
                pos = np.array([x,y])
                mpos = mpos = self.mappos2mpos(pos)
                for direction in range(4):
                    if self.get_wall_state(pos, direction):
                        self.draw_wall(pos, direction)
                if self.m[mpos[1], mpos[0]] == CARD:
                    self.draw_card(pos)

    def set_card(self, pos):
        mpos = self.mappos2mpos(pos)
        self.m[mpos[1], mpos[0]] = CARD

    def show(self, delay=0):
        cv2.imshow("img", self.img)
        cv2.waitKey(delay)
    
    def save_img(self, filename='maze.jpg'):
        cv2.imwrite(filename, self.img)

    def mappos2mpos(self, pos):
        return 2*pos+1

    def build_wall(self, pos, direction):
        mpos = self.mappos2mpos(pos)
        wallPos = mpos + direction2vector[mpos]
        self.m[wallPos[1], wallPos[0]] = WALL

    def destroy_wall(self, pos, direction):
        mpos = self.mappos2mpos(pos)
        wallPos = mpos + direction2vector[direction]
        self.m[wallPos[1], wallPos[0]] = EMPTY

    def get_wall_state(self, pos, direction):
        mpos = self.mappos2mpos(pos)
        wallPos = mpos + direction2vector[direction]
        return self.m[wallPos[1], wallPos[0]] == WALL

    def get_surrounding(self, pos):
        res = []
        for direction in range(4):
            if not self.outofmap(pos, direction):
                res.append(nextPos)
        return res
    
    def outofmap(self, pos, direction):
        nextPos = pos + direction2vector[direction]
        if (nextPos < 0).any() or (nextPos >= 5).any():
            return True
        else:
            return False

    def save_csv(self, filename='map.csv'):
        np.savetxt(filename, self.m, fmt='%d', delimiter=',')

def __main():
    m = Map()
    #测试
    m.outofmap(np.array([0,4]),2)
    m.destroy_wall(np.array([2, 4]), UP)
    m.set_card(np.array([2,2]))
    m.draw_map()
    m.show()
    m.save_img()
    m.save_csv()

if __name__ == '__main__':
    __main()