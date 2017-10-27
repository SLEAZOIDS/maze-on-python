import sys
import copy
import random
import numpy
from preview import *

c = 4
debug = False

class Walker:
    
    def __init__(self, maze_map):
        self.maze_map = maze_map
        # マップ上の進める方向をリストに 0:左  1:下  2:右  3:上
        self.__create_actions((10,10))
        self.__get_initial_actions()

        # moveは移動による座標の増減 0:左  1:下  2:右  3:上
        self.moves = {0: numpy.array([0, -1]), 1: numpy.array([1, 0]), 2: numpy.array([0, 1]), 3: numpy.array([-1, 0])}
        self.preview = Preview(numpy.array(maze_map), 300, 300)

        self.restart()

    def restart(self):
        if debug: print('*****restart****')
        self.journey = []
        self.point = 36
        self.journey.append((1, 1))
        self.__get_initial_actions()

    def walk(self):
        self.__wark_to_next_coordinate()

        y, x = self.journey[-1]

        # HP減りすぎ
        if self.point <= 32:
            # print('****crisis****')
            self.journey.append('error')
            return

        #goal判定
        if y == 8 and x == 8:
            if self.point >= 50: 
                print()
                print('****SUCCESS!!!****')
                print(self.journey)
                print(self.point)
                sys.exit()
            else:
                if self.point >= 46:
                    print('****cant kill restart:' + str(self.point) + '****')
                self.journey.append('error')
                return


        if len(self.actions[y, x]) == 0: 
            # print('****cant walk restart****')
            self.journey.append('error')
            return

        # 今いるところに戻れないように
        self.__remove_action_to_here(y, x)


    def __wark_to_next_coordinate(self):
        y, x = self.journey[-1]

        # 評価値がプラスの場所をc回まで検索（ランダム要素付与）
        i = 0
        action = self.actions[y, x]
        while i <= c:
            random.shuffle(action)
            move = self.moves.get(action[0])
            next_coordinate = list(self.journey[-1] + move)
            reward = self.maze_map[next_coordinate[0]][next_coordinate[1]]
            if reward >= 0:
                break
            i += 1

        self.journey.append(next_coordinate)
        self.point += reward
        if debug: 
            print(next_coordinate, end=' point: ')
            print(self.point)
            self.preview.show(next_coordinate)

    def __get_initial_actions(self):
        self.actions = numpy.array(copy.deepcopy(self.initial_actions))

    # 現在地に至るルートを消す
    def __remove_action_to_here(self, y, x):
        # 左があれば、左からhereに至るアクションを削除
        if 0 in self.actions[y,x]:
            self.actions[y,x-1].remove(2)
        if 1 in self.actions[y,x]:
            self.actions[y+1,x].remove(3)
        if 2 in self.actions[y,x]:
            self.actions[y,x+1].remove(0)
        if 3 in self.actions[y,x]:
            self.actions[y-1,x].remove(1)

    def __create_actions(self, maze_shape):
        self.initial_actions = []
        maze_h, maze_w = maze_shape

        for j in range(maze_h):
            self.initial_actions.append([])
            for i in range(maze_w):
                action = [0, 1, 2, 3]
                self.__remove_around(action, maze_h, maze_w, j, i)
                self.initial_actions[j].append(action)

        self.__create_wall(1, 1)
        self.__create_wall(1, 3)
        self.__create_wall(3, 1)
        self.__create_wall(4, 7)
        self.__create_wall(6, 1)

    def __create_wall(self, y, x):
        self.initial_actions[y][x+1].remove(0)
        self.initial_actions[y-1][x].remove(1)
        self.initial_actions[y][x-1].remove(2)
        self.initial_actions[y+1][x].remove(3)


    def __remove_around(self, action, maze_h, maze_w, j, i):
        if i == 0:
            action.remove(0)
        if i == maze_w - 1:
            action.remove(2)
        if j == 0:
            action.remove(3)
        if j == maze_h - 1:
            action.remove(1)
