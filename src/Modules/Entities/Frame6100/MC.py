# -*- coding: utf-8 -*-
"""MC module

Structure containing MC field of 6100 frame.
"""
from dataclasses import dataclass
@dataclass
class MC:
    enable = 0 
    moveForw = 0
    moveBack = 0
    rotLeft = 0
    rotRight = 0
    turnLeft = 0
    turnRight = 0
    velocity = 0.0 