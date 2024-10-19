from pygame import Surface
from Globals import *
import math
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

LOOKBACK = 3
MAX_DATA = 255
PARAM_NUMBER = 3
CYCLE = 2000

def create_dataset(dataset):
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
        self._model: keras.Model = keras.models.load_model(r'Simulation\AGV\MlNav\NAV.keras')
        self._data = []
        self._path = []
        self._cycle = 0

    def Init(self, img: Surface):
        self._image = img

    def DetermineFlags(self):
        pass

    def FindPath(self, agvPos: tuple, id):
        self._data.append((agvPos[0], agvPos[1], id))
        if timer.GetTicks() - self._cycle > CYCLE:
            self._cycle += CYCLE
            if len(self._data) > LOOKBACK:
                df = pd.DataFrame(self._data, columns=['Going to ID','Y-coordinate','X-coordinate'])
                df['X-coordinate'] = pd.to_numeric(df['X-coordinate'], errors='coerce')
                df = df.values
                df = df.astype('float32')
                scaler = MinMaxScaler(feature_range=(0, 1))
                dataset = scaler.fit_transform(df)
                toPredict = create_dataset(dataset)
                self._path = scaler.inverse_transform(self._model.predict(toPredict))
                self._path = self._path.tolist()
                yDiff = (self._path[0][1] - agvPos[1])
                xDiff = (self._path[0][0] - agvPos[0])
                self._path[0][0] = (xDiff * 0.5) * self._path[0][0]
                self._path[0][1] = (yDiff * 0.5) * self._path[0][1]

        if(len(self._data)  > MAX_DATA):
            self._data.pop()
        
    def GetPath(self):
        return self._path
