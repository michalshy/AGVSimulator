from Modules.Entities.Frame6100.MC import MC
from Modules.Entities.Frame6100.NNC import NNC
# -*- coding: utf-8 -*-
"""Parameters module

Parameters module is responsible for reading configuration parameters and loading
them inside of project to according modules.
Uses mostly public API which is shared around modules.
"""
class Parameters:
    def __init__(self):
        self._mc = MC()
        self._nnc = NNC()

    def GetNNC(self):
        return self._nnc

    def SetDestTrig(self, destTrig: int):
        self._nnc.goDestTrig = destTrig

    def SetDestID(self, destID: int):
        self._nnc.destID = destID

    def GetRoomPath(self):
        return "./Config/Rooms/room2.png"
