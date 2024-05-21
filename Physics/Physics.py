import math
from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.NNS import NNS
from Simulation.AGV.AGV import AGV


class Physics:
    def __init__(self):
        self.maxSpeed = 100 # = 1 m/s

    def emergencyStop(self, nns: NNS, enc: ENC):
        nns.speed = 0
        self.drainBattery(10, enc)

    def rotate(self, rad, nns: NNS, enc: ENC): # 1 - 45 deegre 
        nns.heading = rad
        self.drainBattery(1, enc)

    def accelerate(self, nns: NNS, enc: ENC):
        if nns.speed < self.maxSpeed:
            nns.speed += 10 # a = 0.1m/s^2
            if nns.speed > self.maxSpeed:
                nns.speed = 6
            self.drainBattery(2, enc)

    def updatePosition(self, nns: NNS, enc: ENC):
        nns.xCoor += math.cos(self.radiansToDegrees(nns.heading)) * nns.speed
        nns.yCoor += math.sin(self.radiansToDegrees(nns.heading)) * nns.speed
        self.drainBattery(1, enc)

    def update(self, nns: NNS, enc: ENC):
        self.updatePosition(nns, enc)
        self.drainBattery(1, enc)

    @staticmethod
    def radiansToDegrees(val):
        return val * 180 / 3.14

    @staticmethod
    def drainBattery(val, enc: ENC):
        enc.batteryValue -= val

    def determineMaxSpeed(self, agv: AGV):
        self.maxSpeed = agv.checkMaxSpeed()