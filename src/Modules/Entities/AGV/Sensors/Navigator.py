import pygame
from Globals import *
from Modules.Dec.Dec import Dec
import threading
from Logger import *
import pandas as pd

from Modules.Presentation import OpcClient
from Modules.Presentation.Parameters import Parameters


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

    def FindPath(self, segments: list):
        params = Parameters()
        enum = OpcClient.ServerEnum()
        opc = OpcClient.OpcClient(params, enum.server)
        opc.ReceiveDataFromServer()
        initial_data = opc.GetInitialData()
        self._dec.SetSegments(segments, initial_data)
        if not self._dec.GetInPrediction():
            self._dec.Start()
            threading.Thread(target=self._dec.PredictPath).start()

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
    
    def DrawPath(self, canvas):
        for coord in self._dec.ReturnPredictedPath():
            pygame.draw.rect(canvas, RED, pygame.Rect(
                PointsInterpolationWidth(coord[0]) + ROOM_W_OFFSET,
                PointsInterpolationHeight(coord[1]) + ROOM_H_OFFSET, 
                3, 
                3
            ))