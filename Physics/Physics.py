import math
from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.NNS import NNS
from Simulation.AGV.AGV import AGV


# Class responsible for changing the state of desired AGV
class Physics:
    def __init__(self, agv: AGV):
        self._agv = agv

    def EmergencyStop(self):
        self._agv.GetNNS().speed = 0
        self.DrainBattery(10, self._agv.GetENC())

    def Rotate(self, rad):  # 1 - 45 deegre
        if self._agv.GetBatteryAvailable():
            self._agv.GetNNS().heading = rad
            self.DrainBattery(1, self._agv.GetENC())

    def Accelerate(self):
        if not self._agv.GetAtMaxSpeed() and self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed += 10  # a = 0.1m/s^2
            self.DrainBattery(200, self._agv.GetENC())

    def UpdatePosition(self):
        self._agv.GetNNS().xCoor += round(math.cos(self.RadiansToDegrees(self._agv.GetNNS().heading)), 1) * self._agv.GetNNS().speed  # works after rounding
        self._agv.GetNNS().yCoor += round(math.sin(self.RadiansToDegrees(self._agv.GetNNS().heading)), 1) * self._agv.GetNNS().speed  # works after rounding
        self.DrainBattery(1, self._agv.GetENC())

    def UpdateParams(self):
        if not self._agv.GetBatteryAvailable():
            self._agv.GetNNS().speed = 0
            self.DrainBattery(5, self._agv.GetENC())

    def Update(self):
        self.UpdatePosition()
        self.UpdateParams()

    @staticmethod
    def RadiansToDegrees(val):
        return val * 180 / 3.14

    @staticmethod
    def DrainBattery(val, enc: ENC):
        enc.batteryValue -= val

