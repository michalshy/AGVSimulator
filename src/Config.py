import math
import tomllib
from dataclasses import dataclass
# -*- coding: utf-8 -*-
"""Config module

Contains config and handle all additional functionalities around it.
"""

config = ''
with open("Config.toml", "rb") as f:
    config = tomllib.load(f)

def Degrees(x):
    return math.degrees(x)

def PointsInterpolationWidth(x):
    output = Additional.MATRIX_X[0][1] + (x - Additional.MATRIX_X[0][0]) \
    * (( Additional.MATRIX_X[1][1] -  Additional.MATRIX_X[0][1]) / \
       ( Additional.MATRIX_X[1][0] -  Additional.MATRIX_X[0][0]))
    return output

def PointsInterpolationHeight(y):
    output =  Additional.MATRIX_Y[0][1] + (y - Additional.MATRIX_Y[0][0]) \
    * ((Additional.MATRIX_Y[1][1] - Additional.MATRIX_Y[0][1]) / \
       (Additional.MATRIX_Y[1][0] - Additional.MATRIX_Y[0][0]))
    return output

#COLORS
BLACK = (0,0,0)
WHITE = (255,255,255)
GREEN = (0,255,0)
RED = (255,0,0)

@dataclass
class Additional:
    ROOM_W_OFFSET = (config['screen']['screen_width'] - \
                    config['room']['room_width'])/2
    ROOM_H_OFFSET = (config['screen']['screen_height'] - \
                    config['room']['room_height'])/2

    MATRIX_X = [[config['navigation']['min_x'], 0], \
                              [config['navigation']['max_x'], config['room']['room_width']]]
    MATRIX_Y = [[config['navigation']['min_y'], 0], \
                              [config['navigation']['max_y'], config['room']['room_height']]]

    INFO_WINDOW_POSX = config['screen']['screen_width'] - 275
    INFO_WINDOW_POSY = config['screen']['screen_height'] - 175