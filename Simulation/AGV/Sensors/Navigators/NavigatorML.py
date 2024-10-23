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
    LOOKBACK = 10
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

        self._toDrive = []
        self._data = []
        self._path = []
        self._cycle = 0
        self._appendCycle = 0
        self._distance = 0
        self._headingRad = 0.36016902327537537
        self._stopFlag = False

        #static appending temporary
        if ENGINE == ENGINES.OLEK:
            df = pd.read_csv(r'Resources\agv.pkl', low_memory=False)
            df = df[['X-coordinate', 'Y-coordinate', 'Heading', 'Current segment']]
            df['X-coordinate'] = pd.to_numeric(df['X-coordinate'], errors='coerce')
            df['Y-coordinate'] = pd.to_numeric(df['Y-coordinate'], errors='coerce')
            df['Current segment'] = pd.to_numeric(df['Current segment'], errors='coerce')
            df['Heading'] = pd.to_numeric(df['Heading'], errors='coerce')
            df = df.dropna()
            df = df[df['Current segment'] == 59.0]
            print(df)
            self._scaler = MinMaxScaler()
            df_scaled = df.copy()
            df_scaled[['X-coordinate', 'Y-coordinate', 'Current segment', 'Heading']] = self._scaler.fit_transform(df[['X-coordinate', 'Y-coordinate', 'Current segment', 'Heading']])
            self._toDrive = df_scaled.values.tolist()
            for i in range(LOOKBACK):
                self._data.append(self._toDrive[i])
    def Init(self, img: Surface):
        self._image = img

    def DetermineFlags(self):
         if(len(self._path) != 0):
            if self._distance < 10:
                self._path.pop()
                self._stopFlag = True
            else:
                self._stopFlag = False

    def FindPath(self, batteryVal, agvPos: tuple, heading, id):
        if ENGINE == ENGINES.OLEK:
            if(len(self._path) == 0):
                df = pd.DataFrame(self._data, columns=['X-coordinate', 'Y-coordinate', 'Current segment', 'Heading'])
                df = df.values
                df = df.astype('float32')
                toPredict = create_dataset(df)
                predicted = self._model.predict(toPredict)
                self._path = self._scaler.inverse_transform(predicted)
                self._path = self._path.tolist()
            if len(self._path) != 0:
                yDiff = (agvPos[1] - self._path[0][1])
                xDiff = (agvPos[0] - self._path[0][0])
                self._distance = math.sqrt((xDiff*xDiff)+(yDiff*yDiff))
                self._path[0][0] = xDiff + self._path[0][0]
                self._path[0][1] = yDiff + self._path[0][1]
                self._headingRad = self._path[0][3]
                if self._distance < 1:
                    self._data.append(self._path.pop(0))
        
        if(len(self._data)  > MAX_DATA):
            self._data.pop(0)
        
    def GetPath(self):
        return self._path
    
    def GetDistance(self):
        return self._distance
    
    def GetHeading(self):
        print(self._headingRad)
        return math.degrees(self._headingRad)
    
    def GetStop(self):
        return self._stopFlag