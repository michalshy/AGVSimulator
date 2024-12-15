import sys
sys.dont_write_bytecode
from Modules.Entities.AGV.AGV import AGV
from opcua import Client
import opcua
import pandas as pd
from Logger import *
import time

# -*- coding: utf-8 -*-


class ServerUrl():
    localhost = 'opc.tcp://localhost:48060'
    testServer = 'opc.tcp://localhost:4841/freeopcua/server/'
    agvServer = 'opc.tcp://157.158.57.71:48050'

"""OpcClient module

Responsible for communication with OpcServer, provides set of API methods for
simulation to execute during their controlled cycles.
"""

class OpcClient:
    def __init__(self, url: str):
        self._url = url
        self._dataFromServer = 0
        self._nodeId = None
        self._updateStep = 0
        self._stepAmount = 5
        self._frame6000 = None
        self._NNS = None
        self._ENS = None
        self.client = None
        self._temp_data = []
        self._initial_data = pd.DataFrame(columns=['X-coordinate', 'Y-coordinate', 'Heading', 'Current segment'])
        self._nodeId = "ns=2;i="
        self._connected = False
        self._tab = [5,6,7,13]
        
        self.ConnectToServer()


    def ConnectToServer(self):
        try:
            self.client = Client(self._url)
            self.client.connect()
            self._connected = True
            print("Connected to OPC UA server.")
            if self._url == ServerUrl.localhost:
                self._frame6000 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()
                self._NNS = self._frame6000[-5].get_children()
                self._ENS = self._frame6000[-7].get_children()
            elif self._url == ServerUrl.agvServer:
                self._frame6000 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()
                self._NNS = self._frame6000[-4].get_children()
                self._ENS = self._frame6000[-6].get_children()
            else:
                self._tab = [4,5,6,7,8]
        except Exception as e:
            self._connected = False
            print("Failed to connect to OPC UA server:", e)

    def ConnectToLocalhost(self):
        self._url = "opc.tcp://localhost:48060"
        self.client = Client(self._url)
        self.client.connect()
        self.frame6000 = self.client.get_root_node().get_children()[0].get_children()[1].get_children()[1].get_children()    
        self._NNS = self.frame6000[-5].get_children()
        self._ENS = self.frame6000[-6].get_children()

    def StartReception(self,it):
        try:
            if self._url == ServerUrl.agvServer:
                node = self.client.get_node(self._NNS[it])
                value = node.get_value()

                self._temp_data.append(value)
                
                if(it == 13): # TODO: CHECK ENS BATTERY CELL VOLTAGE SIGNAL
                 temp = pd.DataFrame([[self._temp_data[0],self._temp_data[1],self._temp_data[2],self._temp_data[3], self._temp_data[4]]], columns=['X-coordinate', 'Y-coordinate', 'Heading', 'Current segment','Battery cell voltage'])
                 self._initial_data = pd.concat([self._initial_data,temp])
                 self._temp_data = []
            elif self._url == ServerUrl.testServer:
                node = self.client.get_node(self._nodeId + str(it))
                value = node.get_value()

                self._temp_data.append(value)
            
                if(it == 8):
                    temp = pd.DataFrame([[self._temp_data[0],self._temp_data[1],self._temp_data[2],self._temp_data[3],self._temp_data[4]]], columns=['X-coordinate', 'Y-coordinate', 'Heading', 'Current segment','Battery cell voltage'])
                    self._initial_data = pd.concat([self._initial_data,temp])
                    self._temp_data = []
            
            
            
          
            
        except Exception as e:
            print("Error during StartReception:", e)
            self.ConnectToServer()

    def CloseConnection(self):
        self.client.disconnect()       

    #Receive data from server
    def ReceiveDataFromServer(self):
        if self.client is None:
            self.ConnectToServer()

        if self.client is not None:
            # tab = [5,6,7]
            try:
                for  i in range(20):
                    for j in self._tab:
                        self.StartReception(j)
                    time.sleep(2)
                print(self._initial_data)
                self.CloseConnection()
                return self._initial_data
            except ConnectionResetError:
                print("Connection was reset. Attempting to reconnect...")
                self.ConnectToServer()

    def Transmit(self,input,it):
        if it == 13 or it == 1:
            input = opcua.ua.DataValue(opcua.ua.Variant(int(input), opcua.ua.VariantType.UInt16))
        else:
            input = opcua.ua.DataValue(opcua.ua.Variant(input, opcua.ua.VariantType.Float))

        if it == 1:
            node = self.client.get_node(self._ENS[it])
            node.set_value(input)
        else:
            node = self.client.get_node(self._NNS[it])
            node.set_value(input)
        # self._nodeId = "ns=2;i="   

    #Send to server
    def SendToServer(self, agv: AGV):
        tab = [5,6,7,13,1]  
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
            i+=1
            self.Transmit(agv.GetENS().batteryCellVolt,tab[i])
            self._updateStep = 0
        self._updateStep += 1  
    
    def GetInitialData(self):
            return self._initial_data
    
    def GetStatus(self):
        return self.client
    
    def GetTrStatus(self):
        return self._connected