from pygame import Surface
from Globals import *
from Modules.Entities.Frame6000.NNS import NNS
import tensorflow as tf
import keras
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import pandas as pd
from Modules.Simulation.Logic.Timer import *
import math
from enum import Enum

class Navigator():
    def __init__(self):
        pass

    def Init(self):
        pass

    def DetermineFlags(self):
        pass

    def FindPath(self):
        pass
        
    def GetPath(self):
        return (0,0,0,0,0)
    
    def GetDistance(self):
        return 0
    
    def GetHeading(self):
        return 10
    
    def GetStop(self):
        pass