# -*- coding: utf-8 -*-
"""ENC module

Structure containing ENC field of 6000 frame.
"""
from dataclasses import dataclass
@dataclass
class ENS:
    momentCurrConsump = 0
    batteryCellVolt = 0
    momentPowerConsump = 0
    momentEnergyConsump = 0
    cumulativeEnergyConsump = 0
    batteryValue = 0
    totalEnergyConsump = 0