import threading
from Logger import *
from Modules.Simulation.Logic.Timer import *
from Modules.Presentation.Network.OpcClient import OpcClient, ServerUrl
from Modules.Entities.AGV.AGV import AGV
from Modules.Presentation.Network.TMS.TMS import TMS
from Config import *
import pandas as pd
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
        self._opcRead = OpcClient(ServerUrl.server)
        self._opcWrite = OpcClient(ServerUrl.localhost)

        self._rxTime = 0
        self._txTime = 0

        self._eot = False

        # Threads section
        self._tms_thread = threading.Thread(target=self._tms.Run)
        self._tms_thread.start()
        #--------EOS--------

    def HandleNetwork(self, agv: AGV):
        initial = pd.read_csv('initial_data.csv') # TODO:TEMPORARY
        agv.SetData(initial)                       # TODO:TEMPORARY
        while not self._eot:
            self.HandleRx(agv)
            if self._opcWrite.GetTrStatus():
                self.HandleTx(agv)
        
        self._tms.EndTransmission()
        self._tms_thread.join()
        logger.Debug("TMS thread joined")

    def HandleRx(self, agv: AGV):
        if timer.GetTicks() > (self._rxTime + config['simulation']['sim_rx_cycle']):
            self._rxTime = timer.GetTicks()
            if self._tms.CheckForOrders():
                agv.SetOrder(True, self._tms.GetOrder())
                

    def HandleReadingData(self, agv: AGV):
        if self._opcRead.GetTrStatus():
            agv.SetData(self._opcRead.ReceiveDataFromServer())

    def HandleTx(self, agv: AGV):
        if timer.GetTicks() > (self._txTime + config['simulation']['sim_tx_cycle']):
            self._txTime = timer.GetTicks()
            self._opcWrite.SendToServer(agv)

    def EndTransmission(self):
        self._eot = True

    def CloseConns(self):
        if self._opcRead.GetTrStatus():
            self._opcRead.CloseConnection()
        if self._opcWrite.GetTrStatus():
            self._opcWrite.CloseConnection()
