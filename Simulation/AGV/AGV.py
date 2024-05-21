from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.SS import SS
from Simulation.Frame6000.NNS import NNS


class AGV:
    def __init__(self):
        self._enc = ENC()
        self._ss = SS()
        self._nns = NNS()
        self._maxSpeed = 6

    def checkMaxSpeed(self):
        return self._maxSpeed

    def getENC(self):
        return self._enc

    def getSS(self):
        return self._ss

    def getNNS(self):
        return self._nns

    def printState(self):
        print("Heading: " + str(self._nns.heading))
        print("Speed: " + str(self._nns.speed))
        print("X position: " + str(self._nns.xCoor))
        print("Y position: " + str(self._nns.yCoor))
        print("Battery value: " + str(self._enc.batteryValue))


