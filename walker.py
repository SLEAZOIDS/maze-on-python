import copy
import random
import numpy
from preview import *

class Walker:
    
    def __init__(self, maze_map, initial_actions, moves):
        self.maze_map = maze_map
        self.initial_actions = initial_actions
        self.moves = moves
        self.preview = Preview(numpy.array(maze_map), 300, 300)
        self.restart()

    def restart(self):
        self.journey = []
        self.point = 36
        self.journey.append((1, 1))
        self.actions = copy.deepcopy(self.initial_actions)

    def walk(self):
        if self.point <= 32:
            print('****crisis****')
            self.journey.append('error')
            return

        y, x = self.journey[-1]

        #goal判定
        if x == 8 and y == 8:
            if self.point >= 50: 
                print()
                print('****SUCCESS!!!****')
                print(self.journey)
                print(self.point)
                sys.exit()
            else:
                if self.point >= 48:
                    print()
                    print('****cant kill restart:' + str(self.point) + '****')
                self.journey.append('error')
                return

        if len(self.actions[y, x]) == 0: 
            print('****cant walk restart****')
            self.journey.append('error')
            return

        action = self.actions[y, x]

        # 現在地に至るルートを消す
        if 0 in self.actions[y,x]:
            self.actions[y,x-1].remove(2)
        if 1 in self.actions[y,x]:
            self.actions[y+1,x].remove(3)
        if 2 in self.actions[y,x]:
            self.actions[y,x+1].remove(0)
        if 3 in self.actions[y,x]:
            self.actions[y-1,x].remove(1)
        
        # 評価値の高い場所が見つかるまで進まない
        i = 0
        while i <= 4:
            random.shuffle(action)
            move = self.moves.get(action[0])
            next_coordinate = list(self.journey[-1] + move)
            r = self.maze_map[next_coordinate[0]][next_coordinate[1]]
            if r >= 0:
                break
            i += 1
        
        if next_coordinate not in self.journey:
            self.journey.append(next_coordinate)
            dy, dx = self.journey[-1]
            print(next_coordinate, end=' point: ')
            print(self.point)
            self.point += r
            self.preview.show(next_coordinate)
