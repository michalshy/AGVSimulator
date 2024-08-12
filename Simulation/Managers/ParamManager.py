from Simulation.Frames.Frame6100.NNC import NNC
from Simulation.Frames.Frame6100.MC import MC


# Class for reading variables from server
class ParamManager:
    def __init__(self):
        self._mc = MC()
        self._nnc = NNC()

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

    def GetRoomPath(self):
        return "./Resources/room.png"
