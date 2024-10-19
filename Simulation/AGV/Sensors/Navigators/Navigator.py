from pygame import Surface
from Globals import *
import math
import heapq
from Simulation.Frames.Frame6000.NNS import NNS
from Simulation.Managers.CoordManager import CoordManager

class Navigator:
    def __init__(self) -> None:
        self._image: Surface = None
        self._path: list = []

    def GetAngle(self, a, b, c):
        ang = math.degrees(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1], c[0]-b[0]))
        return ang + 360 if ang < 0 else ang
    
    def CalculateTurn(self, nns: NNS):
        print(nns.xCoor + 25 * math.cos(math.radians(nns.heading)))
        retVal = 0

        pointBeginning = (nns.xCoor, nns.yCoor)
        pointHeading = (nns.xCoor + 25 * math.cos(math.radians(nns.heading)), nns.yCoor + 25 * math.sin(math.radians(nns.heading)))

        if(len(self._path) != 0):
            self.noPathFlag = False
            retVal = self.GetAngle(self._path[0], pointBeginning, pointHeading)
            # Check Distance
            distance = math.sqrt(math.pow(pointBeginning[0] - pointHeading[0], 2) + math.pow(pointBeginning[1] - pointHeading[1], 2))
            if (distance < 5):
                retVal = 0
        else:
            self.noPathFlag = True

        return retVal