import pandas as pd
from Modules.Dec.PathSingleton import PathSingleton
from Logger import *
from Modules.Dec.PredictionModel import PredicitonModel
import multiprocessing as mp
from multiprocessing import Manager, Process, Pipe
import time



# -*- coding: utf-8 -*-
"""Dec module

Deep learning class module, contains method which makes prediction of path possible.
Navigator module within AGV uses it to checks next points on route based on order.
"""

class Dec:
    def __init__(self) -> None:
        self._model = PredicitonModel()
        self._path = []
        self._segments = []
        self._finished = True
        self._started = False
        self._initial_data = []
        self._parent_conn, self._child_conn = Pipe()
        self._process = Process(target=self._model.predict_route, args=(self._child_conn,), daemon=True)
        self._process.start()

    def Start(self):
        print("init")

        self._finished = False
        self._started = True

    def SetSegments(self, segments):
        self._segments = segments
    def SetInitialData(self, initial_data: pd.DataFrame):
        self._initial_data = initial_data

    def PredictPath(self):
        self.Start()
        self._parent_conn.send(["predict",self._initial_data.to_dict(), 20, self._segments])

    def CheckAppend(self):
        # Odczytaj współdzielone dane
        if self._parent_conn.poll():
            el = self._parent_conn.recv()
            if el == "END":
                self._finished = True
                self._started = False
            else:
                # ------------------------------ CRITICAL SECTION ------------------------------
                PathSingleton().Append(el[0])
                self._initial_data = pd.DataFrame(el[1])
                # --------------------------- END OF CRITICAL SECTION ---------------------------
        

    def GetInPrediction(self):
        return (not self._finished) and self._started 

    def ReturnPredictedPath(self):
        # ------------------------------ CRITICAL SECTION ------------------------------
        self._path = PathSingleton().Return()
        # --------------------------- END OF CRITICAL SECTION ---------------------------
        return self._path

    def IsStarted(self):
        return self._started
    
    def PopFront(self):
        # ------------------------------ CRITICAL SECTION ------------------------------
        self._path = PathSingleton().PopFront()
        # --------------------------- END OF CRITICAL SECTION ---------------------------

    def CloseConns(self):
        self._parent_conn.send({"stop"})
        self._parent_conn.close()
        self._child_conn.close()
        self._process.terminate()
    