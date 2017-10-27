from collections import deque
import heapq
import itertools
import numpy
from walker import *

def create_actions(maze_shape):
    actions = []
    maze_h, maze_w = maze_shape

    for j in range(maze_h):
        actions.append([])
        for i in range(maze_w):
            action = [0, 1, 2, 3]
            remove_actions(action, maze_h, maze_w, j, i)
            actions[j].append(action)

    actions = create_wall(actions, 1, 3)
    actions = create_wall(actions, 3, 1)
    actions = create_wall(actions, 4, 7)
    actions = create_wall(actions, 6, 1)
    
    return numpy.array(actions)

def create_wall(actions, y, x):
    actions[y][x+1].remove(0)
    actions[y-1][x].remove(1)
    actions[y][x-1].remove(2)
    actions[y+1][x].remove(3)
    return actions


def remove_actions(action, maze_h, maze_w, j, i):
    if i == 0:
        action.remove(0)
    if i == maze_w - 1:
        action.remove(2)
    if j == 0:
        action.remove(3)
    if j == maze_h - 1:
        action.remove(1)

if __name__ == '__main__':
    maze_map = [
        [-1,1,1,-1,-1,1,1,-1,-1,1],
        [1,0,1,-100,-1,-1,-1,-1,-1,-1],
        [-1,-1,-1,1,1,-1,1,-1,1,1],
        [1,-100,-1,-1,1,-1,1,-1,1,-1],
        [-1,1,1,-1,-1,-1,-1,-100,1,-1],
        [1,-1,1,-1,-1,1,-1,1,-1,1],
        [-1,-100,-1,-1,-1,1,-1,-1,-1,1],
        [-1,1,-1,1,1,-1,1,-1,-1,-1],
        [-1,1,-1,-1,-1,1,1,-1,0,1],
        [-1,-1,1,1,-1,-1,-1,1,-1,-1]
    ]

    # マップ上の進める方向をリストに 0:左  1:下  2:右  3:上
    initial_actions = create_actions((10,10))

    # moveは移動による座標の増減 0:左  1:下  2:右  3:上
    moves = {0: numpy.array([0, -1]), 1: numpy.array([1, 0]), 2: numpy.array([0, 1]), 3: numpy.array([-1, 0])}

    walker = Walker(maze_map, initial_actions, moves)

    while True:
        walker.walk()
        if walker.journey[-1] == 'error':
            walker.restart()
            global actions
            actions = copy.deepcopy(initial_actions)
