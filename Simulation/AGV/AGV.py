from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.SS import SS
from Simulation.Frame6000.NNS import NNS


class AGV:
    def __init__(self):
        self._enc = ENC()
        self._ss = SS()
        self._nns = NNS()

        self._enc.batteryValue = 1000
        self._nns.heading = 4

    def getENC(self):
        return self._enc

    def getSS(self):
        return self._ss

    def getNNS(self):
        return self._nns

    def printState(self):
        print("Heading: " + str(self._nns.heading) + "rad")
        print("Speed: " + str(self._nns.speed/100)+ "m/s")
        print("X position: " + str(round(self._nns.xCoor/100,2))+ "m")
        print("Y position: " + str(round(self._nns.yCoor/100,2))+ "m")
        print("Battery value: " + str(self._enc.batteryValue)+ "mAh")


