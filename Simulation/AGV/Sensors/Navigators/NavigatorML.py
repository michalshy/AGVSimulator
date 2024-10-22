from pygame import Surface
from Globals import *
import heapq
import queue
from Simulation.Frames.Frame6000.NNS import NNS
from Simulation.Managers.CoordManager import CoordManager
import tensorflow as tf
import keras
from Simulation.AGV.Sensors.Navigators.Navigator import Navigator
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from Simulation.Logic.Timer import *
import math
from enum import Enum

class ENGINES(Enum):
    OLEK = 1
    JAKUB = 2

ENGINE = ENGINES.OLEK

if ENGINE == ENGINES.OLEK: # OLEK
    LOOKBACK = 3
    PARAM_NUMBER = 5
    PREDICT_CYCLE = 25
    POSITION_CYCLE = 25

elif ENGINE == ENGINES.JAKUB: # JAKUB
    LOOKBACK = 10
    PARAM_NUMBER = 3
    PREDICT_CYCLE = 200
    POSITION_CYCLE = 500

MAX_DATA = 15


def create_dataset(dataset):
    #ENGINE CONDITIONAL
    if ENGINE == ENGINES.OLEK:
        data = []
        temp = []
        for j in reversed(range(LOOKBACK)):
            a = dataset[len(dataset) - j - 1]
            temp.append(a)
        data.append(temp)
        return np.array(data)
    if ENGINE == ENGINES.JAKUB:
        data = []
        temp = []
        for j in range(3):
            a = dataset[len(dataset) - 1 - LOOKBACK: len(dataset) - 1, j]
            temp.append(a)
        data.append(temp)
        return np.array(data)

class NavigatorML(Navigator):
    def __init__(self) -> None:
        super().__init__()
        self._model: keras.Model
        #ENGINE CONDITIONAL
        if ENGINE == ENGINES.OLEK:
            self._model: keras.Model = keras.models.load_model(r'Simulation\AGV\MlNav\NAVO.keras')
        elif ENGINE == ENGINES.JAKUB:
            self._model: keras.Model = keras.models.load_model(r'Simulation\AGV\MlNav\NAVJ.keras')

        self._data = []
        self._path = []
        self._cycle = 0
        self._appendCycle = 0
        self._distance = 0
        self._headingRad = 0

    def Init(self, img: Surface):
        self._image = img

    def DetermineFlags(self):
        pass

    def FindPath(self, batteryVal, agvPos: tuple, heading, id):
        if timer.GetTicks() - self._appendCycle > POSITION_CYCLE:
            self._appendCycle += POSITION_CYCLE
            if ENGINE == ENGINES.OLEK:
                self._data.append((batteryVal, agvPos[0], agvPos[1], id, math.radians(heading)))
            elif ENGINE == ENGINES.JAKUB:
                self._data.append((agvPos[0], agvPos[1], math.radians(heading)))
        if timer.GetTicks() - self._cycle > PREDICT_CYCLE:
            self._cycle += PREDICT_CYCLE
            if len(self._data) > LOOKBACK:
                #ENGINE CONDITIONAL
                if ENGINE == ENGINES.OLEK:
                    df = pd.DataFrame(self._data, columns=['Battery cell voltage', 'X-coordinate', 'Y-coordinate', 'Going to ID', 'Heading'])
                elif ENGINE == ENGINES.JAKUB:
                    df = pd.DataFrame(self._data, columns=['X-coordinate', 'Y-coordinate', 'Going to ID'])
                df['X-coordinate'] = pd.to_numeric(df['X-coordinate'], errors='coerce')
                df = df.values
                df = df.astype('float32')
                scaler = MinMaxScaler(feature_range=(0, 1))
                dataset = scaler.fit_transform(df)
                toPredict = create_dataset(dataset)
                self._path = scaler.inverse_transform(self._model.predict(toPredict))
                self._path = self._path.tolist()
                #ENGINE CONDITIONAL
                if ENGINE == ENGINES.OLEK:
                    yDiff = (agvPos[1] - self._path[0][2])
                    xDiff = (agvPos[0] - self._path[0][1])
                    self._distance = math.sqrt((xDiff*xDiff)+(yDiff*yDiff))
                    self._path[0][1] = xDiff + self._path[0][1]
                    self._path[0][2] = yDiff + self._path[0][2]
                    self._headingRad = self._path[0][4]
                elif ENGINE == ENGINES.JAKUB:
                    yDiff = (self._path[0][1] - agvPos[1])
                    xDiff = (self._path[0][0] - agvPos[0])
                    self._distance = math.sqrt((xDiff*xDiff)+(yDiff*yDiff))
                    #self._path[0][0] = xDiff + self._path[0][0]    
                    #self._path[0][1] = yDiff + self._path[0][1]
                    self._headingRad = self._path[0][2]
        
        if(len(self._data)  > MAX_DATA):
            self._data.pop(0)
        
    def GetPath(self):
        return self._path
    
    def GetDistance(self):
        return self._distance
    
    def GetHeading(self):
        return math.degrees(self._headingRad)
