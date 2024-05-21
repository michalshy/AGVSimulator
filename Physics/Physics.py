import math
from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.NNS import NNS
from Simulation.AGV.AGV import AGV


# Class responsible for changing the state of desired AGV
class Physics:
    def __init__(self):
        self.maxSpeed = 140  # = 1,4 m/s

    def EmergencyStop(self, nns: NNS, enc: ENC):
        nns.speed = 0
        self.DrainBattery(10, enc)

    def Rotate(self, rad, nns: NNS, enc: ENC):  # 1 - 45 deegre
        nns.heading = rad
        self.DrainBattery(1, enc)

    def Accelerate(self, nns: NNS, enc: ENC):
        if nns.speed < self.maxSpeed:
            nns.speed += 10  # a = 0.1m/s^2
            self.DrainBattery(2, enc)

    def UpdatePosition(self, nns: NNS, enc: ENC):
        nns.xCoor += round(math.cos(self.RadiansToDegrees(nns.heading)), 1) * nns.speed  # works after rounding
        nns.yCoor += round(math.sin(self.RadiansToDegrees(nns.heading)), 1) * nns.speed  # works after rounding
        self.DrainBattery(1, enc)

    def Update(self, nns: NNS, enc: ENC):
        self.UpdatePosition(nns, enc)
        self.DrainBattery(1, enc)

    @staticmethod
    def RadiansToDegrees(val):
        return val * 180 / 3.14

    @staticmethod
    def DrainBattery(val, enc: ENC):
        enc.batteryValue -= val

    def determineMaxSpeed(self, agv: AGV):
        # TODO: Implementation
        pass
