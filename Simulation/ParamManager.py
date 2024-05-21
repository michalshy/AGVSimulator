from Simulation.Frame6100.NNC import NNC
from Simulation.Frame6100.MC import MC


# Class for reading variables from and to server
# TODO: Implementation
class ParamManager:
    def __init__(self):
        self._mc = MC()
        self._nnc = NNC()

    def fabricateFrames(self):
        self._nnc.goDestTrig = 0
        self._nnc.destID = 0

        self._mc.enable = 0
        self._mc.rotLeft = 0
        self._mc.rotRight = 0
        self._mc.turnLeft = 0
        self._mc.turnRight = 0
        self._mc.moveBack = 0
        self._mc.moveForw = 0
        self._mc.velocity = 0

    def SetENC(self):
        pass

    def SetNNS(self):
        pass

    def SetSS(self):
        pass
