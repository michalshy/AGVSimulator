# -*- coding: utf-8 -*-
"""Navigator module

Module which communicates with main deep learning module - Dec and
returns to AGV class.
It is responsible for controlling and holding current paths and upcoming changes in
navigation.
"""
class Navigator():
    def __init__(self):
        pass

    def Init(self):
        pass

    def DetermineFlags(self):
        pass

    def FindPath(self):
        pass
        
    def GetPath(self):
        return (0,0,0,0,0)
    
    def GetDistance(self):
        return 0
    
    def GetHeading(self):
        return 10