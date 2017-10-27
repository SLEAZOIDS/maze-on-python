import numpy
import cv2

# 描画の待ち時間ms
wait = 200

class Preview:
    def __init__(self, maze, height, width):
        self.height, self.width = (height, width)
        self.maze_h, self.maze_w = maze.shape
        self.ystride = height // self.maze_h
        self.xstride = width // self.maze_w
        self.map_org = self.__create_image(maze)
        self.map_now = self.map_org

    def show(self, coordinate):
        self.map_now = self.map_org.copy()
        _y, _x = coordinate
        center = (int((_x + 0.5) * self.xstride), int((_y + 0.5) * self.ystride))
        cv2.circle(self.map_now, center, 11, (255, 255, 255), -1, cv2.LINE_AA)
        cv2.imshow('', self.map_now)
        return cv2.waitKey(wait)

    def __create_image(self, maze):
        image = numpy.zeros((self.height, self.width, 3)).astype('uint8')

        for j in range(self.maze_h):
            for i in range(self.maze_w):
                tl = (self.xstride * i, self.ystride * j)
                br = (self.xstride * (i + 1) - 1, self.ystride * (j + 1) - 1)
                cv2.rectangle(image, tl, br, self.__set_color(maze[j, i]), -1)
        return image

    def __set_color(self, score):
        if score == 1.0:
            return [0, 128, 0]
        elif score == -1.0:
            return [62, 18, 69]
        elif score == -100:
            return [100, 0, 0]
        elif score == 0:
            return [0, 0, 0]
        else:
            return [127, 127, 0]