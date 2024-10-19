from pygame import Surface
from Globals import *
import math
import heapq
from Simulation.Frames.Frame6000.NNS import NNS
from Simulation.Managers.CoordManager import CoordManager

class Navigator:
    def __init__(self) -> None:
        self._image: Surface = None