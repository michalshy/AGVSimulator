from Simulation.Frame6100.NNC import NNC
from Simulation.Frame6100.MC import MC


# Class for reading variables from server
class ParamManager:
    def __init__(self):
        self._mc = MC()
        self._nnc = NNC()
        self.fabricateSimulation()

    def fabricateFrames(self):

        self._mc.enable = 0
        self._mc.rotLeft = 0
        self._mc.rotRight = 0
        self._mc.turnLeft = 0
        self._mc.turnRight = 0
        self._mc.moveBack = 0
        self._mc.moveForw = 0
        self._mc.velocity = 0

    # FABRICATED ROUTES
    def fabricateSimulation(self):
        self._nnc.goDestTrig = 1   # HERE WE EXECUTE TO DRIVE
        self._nnc.destID = 1  # HERE WE PROVIDE INFO ABOUT FABRICATED ROUTES

    def GetNNC(self):
        return self._nnc

    def SetDestTrig(self, destTrig: int):
        self._nnc.goDestTrig = destTrig

    def SetDestID(self, destID: int):
        self._nnc.destID = destID
    def SetENC(self):
        pass

    def SetNNS(self):
        pass

    def SetSS(self):
        pass
