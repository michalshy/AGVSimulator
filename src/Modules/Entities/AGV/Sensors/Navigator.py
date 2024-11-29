import pygame
from Globals import *
from Modules.Dec.Dec import Dec
from Logger import *
import pandas as pd
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
        initial_data = pd.read_csv('initial_data.csv', low_memory=False)
        if self._dec.PredictPath(initial_data,segments):
            logger.Debug("Path predicted")
            self._path = self.GetPath()

        
    def TaskInProgress(self):
        if(len(self._path) != 0):
            return True
        else:
            return False

    def GetPath(self):
        return self._path
    
    def GetDistance(self):
        return 0
    
    def DrawPath(self, canvas):
        for coord in self._path:
            pygame.draw.rect(canvas, RED, pygame.Rect(
                coord[0] * MAP_DENSITY + SCREEN_WIDTH,
                coord[1] * MAP_DENSITY + SCREEN_HEIGHT, 
                5, 
                5
            ))