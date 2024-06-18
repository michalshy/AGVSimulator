from Simulation.Frame6000.ENC import ENC
from Simulation.Frame6000.SS import SS
from Simulation.Frame6000.NNS import NNS
from Simulation.Frame6100.NNC import NNC


# Class that holds state of AGV
class AGV:
    def __init__(self):

        # For frames

        self._enc = ENC()
        self._ss = SS()
        self._nns = NNS()
        self._maxSpeed = 150
        self._enc.batteryValue = 120000
        self._boundryBattery = self._enc.batteryValue * 0.3
        self._nns.heading = 0

        # flags
        self.atMaxSpeed = False
        self.batteryAvailable = True
        self.driveMode = False

        # plotting
        self._histX = []
        self._histY = []

    def GetHistX(self):
        return self._histX

    def GetHistY(self):
        return self._histY

    def SetId(self, nnc: NNC):
        self._nns.goingToID = nnc.destID
        self.driveMode = nnc.goDestTrig

    def DetermineFlags(self):
        if self._nns.speed >= self._maxSpeed:
            self.atMaxSpeed = True
            self._nns.speed = self._maxSpeed
        else:
            self.atMaxSpeed = False

        if self._enc.batteryValue > self._boundryBattery:
            self.batteryAvailable = True
        else:
            self.batteryAvailable = False
            self.driveMode = False


    def GetENC(self):
        return self._enc

    def GetSS(self):
        return self._ss

    def GetNNS(self):
        return self._nns

    def GetMaxSpeed(self):
        return self._maxSpeed

    def GetBatteryAvailable(self):
        return self.batteryAvailable

    def GetAtMaxSpeed(self):
        return self.atMaxSpeed

    def GetDriveMode(self):
        return self.driveMode

    def PrintState(self):
        print("Heading: " + str(self._nns.heading) + "degree")
        print("Speed: " + str(self._nns.speed / 100) + "m/s")
        print("X position: " + str(round(self._nns.xCoor / 100, 2)) + "m")
        print("Y position: " + str(round(self._nns.yCoor / 100, 2)) + "m")
        print("Battery value: " + str(self._enc.batteryValue) + "mAh")

        # for plotting

        self._histX.append(round(self._nns.xCoor / 100, 2))
        self._histY.append(round(self._nns.yCoor / 100, 2))

    def SetDriveMode(self, state: bool):
        self.driveMode = state
