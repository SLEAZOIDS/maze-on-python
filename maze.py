from collections import deque
import heapq
import itertools
import numpy
from walker import *

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

    walker = Walker(maze_map)

    while True:
        walker.walk()
        if walker.journey[-1] == 'error':
            walker.restart()
