import numpy as np
from show_map import *

class Drone:
    def __init__(self, pos = np.array([2, 4]), direction = UP):
        self.pos = pos
        self.direction = direction

    def move_forward(self, m:Map):
        posMoved = self.pos + direction2vector[self.direction]
        if self.pos == np.clip(posMoved, 0, 4) or m.get_wall_state(self.pos, self.direction):
            return False
        else:
            self.pos = posMoved
            return True

    def left(self):
        self.direction = (self.direction - 1) % 4 

    def right(self):
        self.direction = (self.direction + 1) % 4 

class EnvMaze():
    def __init__(self):
        self.maze = Map()
        self.drone = Drone()

    def generate(self):
        startPos=np.array([2,4])
        self.visited = set()
        visitOrder = []
        for y in range(5):
            for x in range(5):
                if x==startPos[0] and y==startPos[1]:
                    continue
                visitOrder.append(np.array([x, y]))
        visitOrder.insert(0, startPos)
        for pos in visitOrder:
            if str(pos) not in self.visited:
                self.dfs_traversal(pos)
        card_counter = 0
        for pos in visitOrder:
            wall_counter = 0
            if (pos == np.array([2,0])).all() or (pos == np.array([2,4])).all():
                continue
            for direction in range(4):
                wall_counter += 1 if self.maze.get_wall_state(pos, direction)==WALL else 0
            if wall_counter == 3:
                self.maze.set_card(pos)
                card_counter += 1
            if card_counter >= 2:
                break
                
        self.maze.draw_map()
        # self.maze.show()
    
    def dfs_traversal(self, pos):
        if str(pos) in self.visited:
            return
        self.visited.add(str(pos))
        for direction in np.random.permutation(4):
            nextPos = pos + direction2vector[direction]
            if not self.maze.outofmap(pos, direction) and str(nextPos) not in self.visited: 
                self.maze.destroy_wall(pos, direction)
                self.dfs_traversal(nextPos)

maze = EnvMaze()
maze.generate()
maze.maze.save_img()
maze.maze.save_csv()