import pygame
from Config import *
from Modules.Dec.Dec import Dec
import threading
from Logger import *
import pandas as pd
import asyncio

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

    def Init(self):
        pass

    def DetermineFlags(self):
        pass

    def FindPath(self, segments: list, initial_data: pd.DataFrame):
        self._dec.SetSegments(segments)
        if(segments[0] == 56.0):
            self._dec.SetInitialData(initial_data)
        if not self._dec.GetInPrediction():
            self._dec.PredictPath()

    def UpdatePath(self):
        self._dec.CheckAppend()

    def TaskInProgress(self):
        if(self._dec.IsStarted()):
            return True
        else:
            return False

    def PopFrontPath(self):
        self._dec.PopFront()

    def GetPath(self):
        return self._dec.ReturnPredictedPath()
    
    def GetDistance(self):
        return 0
    
    def CheckFinished(self):
        return self._dec._finished
    
    def DrawPath(self, canvas):
        for coord in self._dec.ReturnPredictedPath():
            pygame.draw.rect(canvas, RED, pygame.Rect(
                PointsInterpolationWidth(coord[0]) + Additional.ROOM_W_OFFSET,
                PointsInterpolationHeight(coord[1]) + Additional.ROOM_H_OFFSET, 
                3, 
                3
            ))

    def Close(self):
        self._dec.CloseConns()
        logger.Debug("Navigator closed")