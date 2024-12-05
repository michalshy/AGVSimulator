from Modules.Simulation.Logic.Timer import *
from Modules.Entities.Frame6000 import ENC, NNS
from Modules.Entities.AGV import AGV
from Globals import *
from Logger import *
import math
# -*- coding: utf-8 -*-
"""Physics module

Module attached to desired AGV, used to provide simple physics for one vehicle.
It manipulates its fields to simulate real life physic. Does not control vehicle
flags.
"""
class Physics:
    def __init__(self, agv: AGV):
        self._agv = agv

    def Accelerate(self, val):
        if not self._agv.GetAtMaxSpeed() and self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed += val * timer.GetDt() # a = 0.1m/s^2
            self.DrainBattery(2, self._agv.GetENC())
            if(self._agv.GetNNS().speed < 0):
                self._agv.GetNNS().speed = 0

    def UpdatePosition(self):
        self._agv.GetNNS().xCoor += (math.cos(math.radians(self._agv.GetNNS().heading)) * self._agv.GetNNS().speed * timer.GetDt())/1000
        self._agv.GetNNS().yCoor -= (math.sin(math.radians(self._agv.GetNNS().heading)) * self._agv.GetNNS().speed * timer.GetDt())/1000
        self.DrainBattery(1, self._agv.GetENC())


    def UpdateParams(self):
        if not self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed = 0
            self.DrainBattery(5, self._agv.GetENC())

    def Update(self):
        self.UpdatePosition()
        self.UpdateParams()

    def GetAngle(self, a, b, c):
        ang = Degrees(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1], c[0]-b[0]))
        return ang + 360 if ang < 0 else ang

    def CalculateTurn(self, nns: NNS, path):
        retVal = 0
        pointBeginning = (nns.xCoor, nns.yCoor)
        pointHeading = (nns.xCoor + 25 * math.cos(math.radians(nns.heading)), nns.yCoor - 25 * math.sin(math.radians(nns.heading)))
        retVal = self.GetAngle(path, pointBeginning, pointHeading)
        return retVal

    @staticmethod
    def DrainBattery(val, enc: ENC):
        enc.batteryValue -= val
