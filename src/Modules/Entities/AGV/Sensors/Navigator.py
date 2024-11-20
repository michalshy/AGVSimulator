import pygame
from Globals import *
from Modules.Dec.Dec import Dec
# -*- coding: utf-8 -*-
"""Navigator module

Module which communicates with main deep learning module - Dec and
returns to AGV class.
It is responsible for controlling and holding current paths and upcoming changes in
navigation.
"""
class Navigator():
    def __init__(self):
        self._dec = Dec()
        self._path = []

    def Init(self):
        pass

    def DetermineFlags(self):
        pass

    def FindPath(self):
        self._dec.PredictPath()
        
    def GetPath(self):
        self._dec.ReturnPredictedPath()
    
    def GetDistance(self):
        return 0
    
    def GetHeading(self):
        self._dec.ReturnPredictedHeading()
    
    def DrawPath(self, canvas):
        for coord in self._path:
            pygame.draw.rect(canvas, RED, pygame.Rect(coord[0] + ROOM_W_OFFSET, coord[1] + ROOM_H_OFFSET, 5, 5))