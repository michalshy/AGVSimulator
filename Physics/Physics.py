from Simulation.Logic.Timer import *
import math
from Simulation.Frames.Frame6000.ENC import ENC
from Simulation.Frames.Frame6000.NNS import NNS
from Simulation.AGV.AGV import AGV
from Globals import *


# Class responsible for changing the state of desired AGV
class Physics:
    def __init__(self, agv: AGV):
        self._agv = agv

    #TODO: faster the agv, slower the rotate

    def RotateLeft(self):
        if self._agv._nns.speed:
            self._agv.GetNNS().heading += ROTATE_VAL * timer.GetDt()
            self.DrainBattery(1, self._agv.GetENC())
    
    #TODO: faster the agv, slower the rotate
    
    def RotateRight(self):
        if self._agv._nns.speed:
            self._agv.GetNNS().heading -= ROTATE_VAL * timer.GetDt()
            self.DrainBattery(1, self._agv.GetENC())
    
    def Accelerate(self, val):
        if not self._agv.GetAtMaxSpeed() and self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed += val * timer.GetDt() # a = 0.1m/s^2
            self.DrainBattery(2, self._agv.GetENC())
            if(self._agv.GetNNS().speed < 0):
                self._agv.GetNNS().speed = 0

    def UpdatePosition(self):
        self._agv.GetNNS().xCoor += math.cos(math.radians(self._agv.GetNNS().heading)) * self._agv.GetNNS().speed * timer.GetDt()
        self._agv.GetNNS().yCoor += math.sin(math.radians(self._agv.GetNNS().heading)) * self._agv.GetNNS().speed * timer.GetDt()
        self.DrainBattery(1, self._agv.GetENC())

    def UpdateParams(self):
        if not self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed = 0
            self.DrainBattery(5, self._agv.GetENC())

    def Update(self):
        self.UpdatePosition()
        self.UpdateParams()

    @staticmethod
    def DrainBattery(val, enc: ENC):
        enc.batteryValue -= val
