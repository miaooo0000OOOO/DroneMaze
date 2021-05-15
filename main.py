import numpy as np
import cv2

def read_map(filename = ""):
    with open(filename, 'r') as f:


def input_map():
    pass

class Map():
    def __init__(self, mArray, a = 5):
        self.a = a  #边长
        self.mArray = mArray
    
    def write(self, pos, cellArray):
        self.mArray[pos] = cellArray

    def isblocked(self, pos, direction):
        return self.mArray[pos][direction]


class Env():
    def __init__(self, m = input_map()):\
        pass


    