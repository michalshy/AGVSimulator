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
        self._opcRead = OpcClient(ServerUrl.testServer)
        self._opcWrite = OpcClient(ServerUrl.localhost)
        self.initial = None

        self._rxTime = 0
        self._txTime = 0

        self._eot = False


    def HandleNetwork(self, agv: AGV):
        self._tms.Run()
        self.InitializeServerData(agv)
        while not self._eot:
            self.HandleRx(agv)
            if self._opcWrite.GetTrStatus():
                self.HandleTx(agv)
        
        logger.Debug("Network closed")

    def HandleRx(self, agv: AGV):
        if timer.GetTicks() > (self._rxTime + config['simulation']['sim_rx_cycle']):
            self._rxTime = timer.GetTicks()
            if agv._checkOrder:
                agv.SetOrder(True, self._tms.GetOrder())
                agv.SetTimeWait(self._tms.GetTimeWait())
                logger.Debug("Segment passed from TMS")
                index = agv.GetPassingIdx() + 1
                agv.SetPassingIdx(index)
                agv._checkOrder = False

                

    def HandleReadingData(self, agv: AGV):
        if self._opcRead.GetTrStatus():
            agv.SetData(self._opcRead.ReceiveDataFromServer())

    def HandleTx(self, agv: AGV):
        if timer.GetTicks() > (self._txTime + config['simulation']['sim_tx_cycle']):
            self._txTime = timer.GetTicks()
            self._opcWrite.SendToServer(agv)

    def InitializeServerData(self, agv: AGV):
        if self._opcRead._connected == False:
            try:
                self.initial = pd.read_csv('init_data.csv')
            except Exception as e:
                print("Can't read initial_data.csv", e)
        else:
            self.HandleReadingData(agv)
            self.initial = self._opcRead.GetInitialData()
        agv.SetData(self.initial)                      

    def EndTransmission(self):
        self._eot = True

    def CloseConns(self):
        if self._opcRead._connected == True:
            self._opcRead.CloseConnection()
        if self._opcWrite._connected == True:
            self._opcWrite.CloseConnection()
