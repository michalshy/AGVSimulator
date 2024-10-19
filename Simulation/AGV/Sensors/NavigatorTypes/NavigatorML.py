from pygame import Surface
from Globals import *
import math
import heapq
from Simulation.Frames.Frame6000.NNS import NNS
from Simulation.Managers.CoordManager import CoordManager
import tensorflow as tf
import keras
import Navigator

class NavigatorML(Navigator):
    def __init__(self) -> None:
        super().__init__()
        self._model = keras.models.load_model(r'Simulation\AGV\MlNav\NAV.keras')


    def Init(self, img: Surface):
        self._image = img