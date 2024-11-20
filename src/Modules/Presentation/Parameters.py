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
        pass

    def GetRoomPath(self):
        return "./Config/Rooms/room2.png"
