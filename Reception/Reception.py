import socket  # Import socket module
from Simulation.ParamManager import ParamManager
from opcua import Client


class Reception:
    def __init__(self, paramManager: ParamManager):
        self._param_manager = paramManager
        self._url = "opc.tcp://localhost:4841/freeopcua/server/"
        self._nodeId = "ns=2;i="
        self._dataFromServer = 0
        self.value = ""

    def StartReceptionLocal(self):
        self._param_manager.fabricateFrames()

    def StartReception(self,it):
        self._nodeId += str(it)
        self.client = Client(self._url)
        self.client.connect()
        node = self.client.get_node(self._nodeId)
        value = node.get_value()
        self._dataFromServer = value
        self._nodeId = "ns=2;i=" 

    def CloseConnection(self, conn):
        self.client.disconnect()
