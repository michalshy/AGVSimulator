from Modules.Simulation.Logic.Timer import *
from Modules.Entities.Frame6000 import ENS, NNS
from Modules.Entities.AGV import AGV
from Config import *
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
            self.DrainBattery(2, self._agv.GetENS())

    def Slow(self, val):
        if self._agv.ShouldSlow():
            self._agv.GetNNS().speed -= val * timer.GetDt() # a = 0.1m/s^2
            self.DrainBattery(2, self._agv.GetENS())
            if(self._agv.GetNNS().speed < 0):
                self._agv.GetNNS().speed = 0  
        
    def Stop(self):
        self._agv.GetNNS().speed = 0

    def UpdatePosition(self):
        self._agv.GetNNS().xCoor += (math.cos(math.radians(self._agv.GetNNS().heading)) * self._agv.GetNNS().speed * timer.GetDt())/10000
        self._agv.GetNNS().yCoor -= (math.sin(math.radians(self._agv.GetNNS().heading)) * self._agv.GetNNS().speed * timer.GetDt())/10000
        self.DrainBattery(1, self._agv.GetENS())

    def UpdateParams(self):
        if not self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed = 0
            self.DrainBattery(5, self._agv.GetENS())

    def Update(self):
        self.UpdatePosition()
        self.UpdateParams()

    def GetAngle(self, a, b, c):
        ang = Degrees(math.atan2(a[1]-b[1], a[0]-b[0]) - math.atan2(c[1]-b[1], c[0]-b[0]))
        return ang + 360 if ang < 0 else ang
    
    def GetDistance(self, a, b):
        return math.dist(a, b)

    def CalculatePath(self, nns: NNS, path) -> tuple:
        retH = 0
        retD = 0
        pointBeginning = (nns.xCoor, nns.yCoor)
        pointHeading = (nns.xCoor + 25 * math.cos(math.radians(nns.heading)), nns.yCoor - 25 * math.sin(math.radians(nns.heading)))
        retD = self.GetDistance(pointBeginning, (path[0], path[1]))
        retH = self.GetAngle(path, pointBeginning, pointHeading)
        return (retH, retD)

    @staticmethod
    def DrainBattery(val, ens: ENS):
        ens.batteryCellVolt -= val
