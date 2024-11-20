from Modules.Simulation.Logic.Timer import *
from Modules.Presentation.OpcClient import OpcClient
from Modules.Entities.AGV.AGV import AGV
from Globals import *

# -*- coding: utf-8 -*-
"""Network module

This module handles communication with upper layer of OpcClient, which means it
controls when informations are passed to the upper layer. Controls also communication
with Order module, which means is responsible for reception of new orders from TMS
"""
class Network:
    def __init__(self) -> None:
        self._rxTime = 0
        self._txTime = 0

    def HandleNetwork(self):
        self.HandleRx()
        self.HandleTx()

    def HandleRx(self):
        if timer.GetTicks() > (self._cycle + SIMULATION_RX_CYCLE):
            self._rxTime = timer.GetTicks()
            #TODO: TMS HANDLE

    def HandleTx(self, opc: OpcClient, agv: AGV):
        if timer.GetTicks() > (self._cycle + SIMULATION_TX_CYCLE):
            self._txTime = timer.GetTicks()
            opc.SendToServer(agv)