import pygame
from Globals import *
from Modules.Dec.Dec import Dec
from Logger import *
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

    def FindPath(self, segments: list):
        initial_data = [] # TODO 
        self._dec.PredictPath(initial_data,segments)
        logger.Debug("Path predicted")

        self._path = self.GetPath()
        
    def TaskInProgress(self):
        return True

    def GetPath(self):
        return self._dec.ReturnPredictedPath()
    
    def GetDistance(self):
        return 0
    
    def GetHeading(self):
        return self._dec.ReturnPredictedHeading()
    
    def DrawPath(self, canvas):
        for coord in self._path:
            pygame.draw.rect(canvas, RED, pygame.Rect(coord[0], coord[1], 10, 10))