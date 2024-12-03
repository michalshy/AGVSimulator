import sys
sys.dont_write_bytecode
from Modules.Presentation.Parameters import Parameters
from Modules.Entities.AGV.AGV import AGV
from opcua import Client
import opcua
# -*- coding: utf-8 -*-
"""OpcClient module

Responsible for communication with OpcServer, provides set of API methods for
simulation to execute during their controlled cycles.
"""
class OpcClient:
    def __init__(self, params: Parameters):
        self._params = params
        self._url = "opc.tcp://157.158.57.71:48050"
        self._dataFromServer = 0
        self._nodeId = None
        self._updateStep = 0
        self._stepAmount = 5
        self._frame6000 = None
        self._NNS = None
        self._ENS = None
        self.client = None
        self._temp_data = []
        self._initial_data = []
        
        self.ConnectToServer()


    def ConnectToServer(self):
        try:
            self.client = Client(self._url)
            self.client.connect()
            print("Connected to OPC UA server.")
            self.frame6000 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()
            self.NNS = self.frame6000[-4].get_children()
            self._ENS = self.frame6000[-6].get_children()
            self._nodeId = self._NNS
        except Exception as e:
            print("Failed to connect to OPC UA server:", e)

    def ConnectToLocalhost(self):
        self._url = "opc.tcp://localhost:48060"
        self.client = Client(self._url)
        self.client.connect()
        self.frame6000 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()    
        self._NNS = self.frame6000[-5].get_children()
        self._ENS = self.frame6000[-6].get_children()
        self._nodeId = self._NNS
    
    def StartReception(self,it):
        try:
            node = self.client.get_node(self.NNS[it])
            value = node.get_value()
            self.dataReceived += f"{value}"
            self._temp_data.append(value)
            if(it == 13):
                 self._initial_data.append(self._temp_data)
                 self._temp_data = []
            
        except Exception as e:
            print("Error during StartReception:", e)
            self.ConnectToServer()

    def CloseConnection(self):
        self.client.disconnect()       

    #Receive data from server
    def ReceiveDataFromServer(self, params: Parameters):
        if self.client is None:
            self.ConnectToServer()

        if self.client is not None:
            tab = [5,6,7]
            try:
                for  i in range(15):
                    for i in tab:
                        self.StartReception(i)
                self.CloseConnection()
                self.ConnectToLocalhost()
            except ConnectionResetError:
                print("Connection was reset. Attempting to reconnect...")
                self.ConnectToServer()

        
        

    def Transmit(self,input,it):
        if it == 13:
            input = opcua.ua.DataValue(opcua.ua.Variant(input, opcua.ua.VariantType.UInt16))
        else:
            input = opcua.ua.DataValue(opcua.ua.Variant(input, opcua.ua.VariantType.Float))
        node = self.client.get_node(self._NNS[it])
        node.set_value(input)
        # self._nodeId = "ns=2;i="   

    #Send to server
    def SendToServer(self, agv: AGV):
        tab = [5,6,7,13]  
        it = 0   
        i = 0
        if self._updateStep % self._stepAmount == 0:
            self.Transmit(agv.GetNNS().xCoor, tab[i])
            i+=1    
            self.Transmit(agv.GetNNS().yCoor,tab[i])
            i+=1     
            self.Transmit(agv.GetNNS().heading,tab[i])
            i+=1     
            self.Transmit(agv.GetNNS().currSegment,tab[i])
            self._updateStep = 0
        self._updateStep += 1  
    
    def GetInitialData(self):
            return self._initial_data

    def GetStatus(self):
        return self.client