# -*- coding: utf-8 -*-
"""NNC module

Structure containing NNC field of 6100 frame.
"""
from dataclasses import dataclass
@dataclass
class NNC:
    destID = 0 
    goDestTrig = 0 
    pauseDriveTrig = 0
    resumeDriveTrig = 0
    abortDriveTrig = 0