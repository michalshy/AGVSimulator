import threading
from Logger import *
from Modules.Presentation.Parameters import Parameters
from Modules.Simulation.Logic.Timer import *
from Modules.Presentation.OpcClient import OpcClient, ServerUrl
from Modules.Entities.AGV.AGV import AGV
from Modules.Simulation.Network.TMS.TMS import TMS
from Globals import *
import time
# -*- coding: utf-8 -*-
"""Network module

This module handles communication with upper layer of OpcClient, which means it
controls when informations are passed to the upper layer. Controls also communication
with Order module, which means is responsible for reception of new orders from TMS
"""
class Network:
    def __init__(self) -> None:
        self._tms = TMS()
        self._opcRead = OpcClient(Parameters, ServerUrl.server)
        self._opcWrite = OpcClient(Parameters, ServerUrl.localhost)

        self._rxTime = 0
        self._txTime = 0

        self._eot = False

        # Threads section
        self._tms_thread = threading.Thread(target=self._tms.Run)
        self._tms_thread.start()
        #--------EOS--------

    def HandleNetwork(self, agv: AGV):
        while not self._eot:
            self.HandleRx(agv)
            self.HandleTx(agv)
        
        self._tms.EndTransmission()
        self._tms_thread.join()
        logger.Debug("TMS thread joined")

    def HandleRx(self, agv: AGV):
        if timer.GetTicks() > (self._rxTime + SIMULATION_RX_CYCLE):
            self._rxTime = timer.GetTicks()
            if self._tms.CheckForOrders():
                agv.SetOrder(True, self._tms.GetOrder())
                

    def HandleReadingData(self, agv: AGV):
        agv.SetData(self._opcRead.ReceiveDataFromServer())

    def HandleTx(self, agv: AGV):
        if timer.GetTicks() > (self._txTime + SIMULATION_TX_CYCLE):
            self._txTime = timer.GetTicks()
            self._opcWrite.SendToServer(agv)

    def EndTransmission(self):
        self._eot = True
