import socket  # Import socket module
from Simulation.ParamManager import ParamManager
from opcua import Client


class Reception:
    def __init__(self, paramManager: ParamManager):
        self._port = 50000  # placeholder
        self._sock = socket.socket()
        self._host = '127.0.0.1'  # placeholder
        self._data = ''
        self._param_manager = paramManager
        self._url = "opc.tcp://desktop-vics7it:62640/IntegrationObjects/ServerSimulator/"
        self._nodeId = "ns=2;s=Tag"
        self._dataFromServer = []

    def StartReceptionLocal(self):
        self._param_manager.fabricateFrames()

    def StartReception(self,it):
        self._nodeId += str(it)
        client = Client(self._url)
        client.connect()
        node = client.get_node(self._nodeId)
        value = node.get_value()
        self._dataFromServer.append(value)

        self._nodeId = "ns=2;s=Tag" 

    def CloseConnection(self, conn):
        client.disconnect()
