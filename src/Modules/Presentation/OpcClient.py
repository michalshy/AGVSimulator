import sys
sys.dont_write_bytecode
from Modules.Presentation.Parameters import Parameters
from Modules.Entities.AGV import AGV
from opcua import Client
# -*- coding: utf-8 -*-
"""OpcClient module

Responsible for communication with OpcServer, provides set of API methods for
simulation to execute during their controlled cycles.
"""
class OpcClient:
    def __init__(self, params: Parameters):
        self._params = params
        self._url = "opc.tcp://localhost:4841/freeopcua/server/"
        self._dataFromServer = 0
        self._nodeId = "ns=2;i="
        self._updateStep = 0
        self._stepAmount = 5
        self.client = Client(self._url)
        self.client.connect()

    def StartReception(self,it):
        self._nodeId += str(it)
        node = self.client.get_node(self._nodeId)
        value = node.get_value()
        self._dataFromServer = value
        self._nodeId = "ns=2;i=" 

    def CloseConnection(self):
        self.client.disconnect()       

    #Receive data from server
    def ReceiveDataFromServer(self, params: Parameters):
        tab = [13,14]  
        it = 0   
        if self._updateStep % self._stepAmount == 0:
            self.StartReception(tab[it])
            params.SetDestID(self._dataFromServer)
            it+=1
            self.StartReception(tab[it])
            params.SetDestTrig(self._dataFromServer)
            self._updateStep = 0
        self._updateStep += 1    

    def Transmit(self,input,it):
        self._nodeId += str(it)
        node = self.client.get_node(self._nodeId)
        node.set_data_value(input)
        self._nodeId = "ns=2;i="   

    #Send to server
    def SendToServer(self, agv: AGV):
        tab = [7,8,5,10,6]  
        it = 0   
        if self._updateStep % self._stepAmount == 0:
            self.Transmit(agv.GetNNS().xCoor, tab[it])    
            it+=1 
            self.Transmit(agv.GetNNS().yCoor,tab[it])     
            it+=1
            self.Transmit(agv.GetNNS().heading,tab[it])     
            it+=1
            self.Transmit(agv.GetENC().batteryValue,tab[it])     
            it+=1
            self.Transmit(agv.GetNNS().speed,tab[it])     
            self._updateStep = 0
        self._updateStep += 1  

    def GetStatus(self):
        return self.client