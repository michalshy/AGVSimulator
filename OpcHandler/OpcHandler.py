import sys
sys.dont_write_bytecode
from Simulation.ParamManager import ParamManager
from opcua import Client
from Simulation.AGV.AGV import AGV

class OpcHandler:
    def __init__(self, paramManager: ParamManager, agv: AGV):
        self._param_manager = paramManager
        self._url = "opc.tcp://localhost:4841/freeopcua/server/"
        self._dataFromServer = 0
        self._agv = agv
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
    def ReceiveDataFromServer(self):
        tab = [13,14]  
        it = 0   
        if self._updateStep % self._stepAmount == 0:
            self.StartReception(tab[it])
            self._param_manager.SetDestID(self._dataFromServer)
            it+=1
            self.StartReception(tab[it])
            self._param_manager.SetDestTrig(self._dataFromServer)
            self._updateStep = 0
        self._updateStep += 1    

    def Transmit(self,input,it):
        self._nodeId += str(it)
        node = self.client.get_node(self._nodeId)
        node.set_data_value(input)
        self._nodeId = "ns=2;i="   

    #Send to server
    def SendToServer(self):
        tab = [7,8,5,10,6]  
        it = 0   
        if self._updateStep % self._stepAmount == 0:
            self.Transmit(self._agv.GetNNS().xCoor, tab[it])    
            it+=1 
            self.Transmit(self._agv.GetNNS().yCoor,tab[it])     
            it+=1
            self.Transmit(self._agv.GetNNS().heading,tab[it])     
            it+=1
            self.Transmit(self._agv.GetENC().batteryValue,tab[it])     
            it+=1
            self.Transmit(self._agv.GetNNS().speed,tab[it])     
            self._updateStep = 0
        self._updateStep += 1   